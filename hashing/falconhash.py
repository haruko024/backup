import sys
import argparse
import threading
import queue

import length6, length7, length8, length9, length10, length11, length12, length13, length14


def run_module(module, pcap_file, result_queue, found_event, lock):
    result = module.run(pcap_file, found_event)
    if result:
        with lock:
            if not found_event.is_set():
                found_event.set()
                result_queue.put((module.__name__, result))

def main():
    parser = argparse.ArgumentParser(description="FalconHash: Brute-force hash cracking for specific lengths.")
    parser.add_argument("-hc", "--hashcrack", required=True, help="Path to .cap file to hash and crack")
    args = parser.parse_args()

    pcap_file = args.hashcrack
    print(f"🔍 Hashing and cracking: {pcap_file}")

    modules = [length6, length7, length8, length9, length10, length11, length12, length13, length14]
    threads = []
    result_queue = queue.Queue()
    found_event = threading.Event()
    lock = threading.Lock()

    for module in modules:
        t = threading.Thread(target=run_module, args=(module, pcap_file, result_queue, found_event, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not result_queue.empty():
        module_name, password = result_queue.get()
        print(f"[✅] Password cracked by {module_name}: \"{password}\"")
    else:
        print("[❌] Password not found in length 6–14 range.")

if __name__ == "__main__":
    main()
