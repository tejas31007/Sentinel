#include <iostream>
#include <vector>
#include <pcap.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <cstdlib> // For system() commands
#include <string>
#include "onnxruntime_cxx_api.h"
#include <fstream> // Add this include

void log_to_file(std::string src_ip) {
    std::ofstream outfile;
    outfile.open("../dashboard_data.txt", std::ios_base::app); // Append mode
    outfile << src_ip << std::endl;
}



Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "SentinelAI");
Ort::SessionOptions session_options;
Ort::Session* session = nullptr;

// --- THE FIREWALL ENFORCER ---
void block_ip(const char* ip_address) {
    // SAFETY CHECK: Don't block your own router or localhost!
    std::string ip_str(ip_address);
    if (ip_str.rfind("192.168.", 0) == 0 || ip_str == "127.0.0.1") {
        std::cout << "[SAFEGUARD] Skipping block for local/safe IP: " << ip_str << std::endl;
        return;
    }

    // The Command: "sudo iptables -A INPUT -s 1.2.3.4 -j DROP"
    std::string command = "iptables -A INPUT -s " + ip_str + " -j DROP";
    
    std::cout << "\033[1;31m[FIREWALL] EXECUTING: " << command << "\033[0m" << std::endl;
    
    // Execute the command in Linux terminal
    system(command.c_str());
}

void packet_handler(u_char *user_data, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    struct ip *ip_header = (struct ip*)(packet + 14);

    if (ip_header->ip_p == IPPROTO_TCP) {
        int ip_header_len = ip_header->ip_hl * 4;
        struct tcphdr *tcp_header = (struct tcphdr*)(packet + 14 + ip_header_len);

        float packet_size = (float)pkthdr->len;
        float src_port = (float)ntohs(tcp_header->source);
        float dst_port = (float)ntohs(tcp_header->dest);
        float flags = (float)tcp_header->th_flags;

        // Convert IP to string for blocking
        char* src_ip_str = inet_ntoa(ip_header->ip_src);

        // AI Logic
        std::vector<float> input_tensor_values = {src_port, dst_port, packet_size, flags};
        std::vector<int64_t> input_node_dims = {1, 4};

        Ort::MemoryInfo memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
        Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
            memory_info, input_tensor_values.data(), input_tensor_values.size(), 
            input_node_dims.data(), input_node_dims.size()
        );

        const char* input_names[] = {"float_input"};
        const char* output_names[] = {"output_label", "output_probability"};

        auto output_tensors = session->Run(
            Ort::RunOptions{nullptr}, input_names, &input_tensor, 1, output_names, 2
        );

        int64_t* label = output_tensors[0].GetTensorMutableData<int64_t>();

        // --- ACTIVE DEFENSE LOGIC ---
        if (*label == 1) {
            std::cout << "[ALERT] Malicious Traffic from " << src_ip_str << " Detected!" << std::endl;
            
            // CALL THE FIREWALL
            block_ip(src_ip_str);
            log_to_file(src_ip_str);
        }
    }
}

int main() {
    std::cout << "Loading AI Brain..." << std::endl;
    session = new Ort::Session(env, "sentinel.onnx", session_options);
    
    char errbuf[PCAP_ERRBUF_SIZE];
    
    // *** CHANGE THIS TO YOUR INTERFACE ***
    const char* dev = "wlo1"; 

    pcap_t *handle = pcap_open_live(dev, 65535, 1, 1000, errbuf);
    if (handle == NULL) {
        std::cerr << "Error: " << errbuf << std::endl;
        return 2;
    }
    
    std::cout << "Sentinel Active Defense System ONLINE on " << dev << "..." << std::endl;
    pcap_loop(handle, 0, packet_handler, NULL);
    pcap_close(handle);
    return 0;
}