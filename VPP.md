# Vector Packet Processing (VPP)

As network speeds have increased from 10 Gbps to 100 Gbps and beyond, traditional methods of packet processing have struggled to keep up. High-speed packet processing is essential for modern applications, particularly those involving media-rich and bandwidth-intensive content. Moreover, modern networks often need to manage very large routing tables, sometimes containing over 500,000 entries. This adds to the complexity and demands of data plane systems.

Using the vanilla Linux kernel for high-speed packet processing requires significant CPU resources and high-end processors, which is not efficient. Historically, custom hardware like ASICs and FPGAs were used to achieve the necessary speeds. However, these solutions have limitations in terms of speed, density, power consumption, and interface complexity.

To overcome these limitations, FD.io (Fast Data – Input/Output) was introduced. FD.io is a universal, cross-platform data plane that is supported by multiple hardware vendors. It provides a secure and efficient framework for high-speed packet processing. Vector Packet Processing (VPP) is the core technology used in FD.io. It achieves high speeds while requiring low computing power. VPP processes packets in vectors (batches) rather than individually, which improves throughput and efficiency.

## DPDK and VPP

VPP relies on DPDK for packet I/O operations. DPDK provides a set of libraries and drivers that allow for fast packet processing in user space, bypassing the kernel to minimize latency and maximize throughput. VPP leverages these capabilities to achieve high-speed packet handling. DPDK handles the reception of packets from the NIC, placing them into memory buffers that VPP can then process. After processing, VPP uses DPDK to transmit packets back through the NIC.

DPDK enables VPP to take full advantage of modern multi-core processors. It allows VPP to allocate CPU cores for specific packet processing tasks, ensuring efficient and parallel processing of network packets. DPDK supports batch processing of packets, which aligns with VPP’s vector-based approach. This method groups packets into vectors (batches) and processes them together, significantly enhancing throughput and reducing per-packet processing overhead. Refer to [dpdk-labnet](https://github.com/ManiAm/dpdk-labnet) project for more information.

## Vector Packet Processing

To understand the concepts of VPP, we first need to understand how packets were processed before VPP.

Scalar packet processing refers to processing one packet at a time. This involves processing an interrupt, calling a set of routines and then deciding on the destiny of the packet. As part of this, we read the packet from the queue, load the instruction set, perform the checks on the packet, unload the instruction set, route the packet, and then repeat the same procedure for the entire set of packets received. When the code path length exceeds the size of the CPU instruction cache (I-cache), thrashing occurs as the CPU is continually loading new instructions. Each packet incurs an identical set of I-cache misses, increasing the time taken for processing each packet which leads to inefficient processing.

Vector packet processing resolves this inefficiency by processing more than one packet at the same time, since all packets have to go through the same instruction set in sequence. This avoids the continuous loading and unloading of the instruction set to and from the cache, thereby reducing the cache misses as well as read latency. As the size of the vector increases, the processing cost per packet reduces. In other words, vector packet processing handles multiple packets simultaneously using single-instruction multiple-data (SIMD) operations whereas scalar packet processing handles packets one at a time, using single-instruction single-data (SISD) operations.

A rough everyday analogy to this would be to consider the problem of a stack of lumber where each piece of lumber needs to be cut, sanded, and have holes drilled in it. You can only have one tool in your hand at a time (analogous to the instruction cache). You are going to finish cutting, sanding, and drilling the lumber faster if you first pick up the saw and do all of your cutting, then pick up the sander and do all of your sanding, and then pick up the drill and do all of your drilling. Picking up each tool in order for each piece of lumber is going to be much slower.

The main advantage of VPP is that it achieves high speeds without requiring multiple processing cores that are needed to achieve the same speeds in traditional Linux processing. Currently FD.io and VPP are being used to build high end virtual Load Balancers, Firewalls, Switches and Routers.
