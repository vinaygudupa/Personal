from os import system

try:
    file_handle = open("/Users/vinay/LoadTest/AMI_with_avmd_fix_22Aug2019/top_process_full_2019-08-22-14:35.log", 'r')
    file_lines = file_handle.readlines()
    system("rm -rf /Users/vinay/LoadTest/AMI_with_avmd_fix_22Aug2019/system_level_usage.csv")
    system_level_usage = open("/Users/vinay/LoadTest/AMI_with_avmd_fix_22Aug2019/system_level_usage.csv", 'a')
    system_level_usage.write("time, cpu_us, cpu_sy, cpu_ni, cpu_id, cpu_wa, cpu_hi, cpu_si, cpu_st, mem_total, mem_used, mem_free, mem_buffers, mem_cached, actual_cpu_used, actual_mem_used, load_avg")
    system_level_usage.write("\n")
    system("rm -rf /Users/vinay/LoadTest/AMI_with_avmd_fix_22Aug2019/process_level_cpu.csv")
    process_level_cpu_usage = open("/Users/vinay/LoadTest/AMI_with_avmd_fix_22Aug2019/process_level_cpu.csv", 'a')
    process_level_cpu_usage.write("time, freeswitch, plivo-cal, plivo-rec, plivo-eve, s3upload, voipmon, redis-ser, pcap-uploader")
    process_level_cpu_usage.write("\n")
    system("rm -rf /Users/vinay/LoadTest/AMI_with_avmd_fix_22Aug2019/process_level_mem.csv")
    process_level_mem_usage = open("/Users/vinay/LoadTest/AMI_with_avmd_fix_22Aug2019/process_level_mem.csv", 'a')
    process_level_mem_usage.write("time, freeswitch, plivo-cal, plivo-rec, plivo-eve, s3upload, voipmon, redis-ser, pcap-uploader")
    process_level_mem_usage.write("\n")

except Exception as e:
    print("Exception occured while opening file : ", str(e))
else:
    cpu_dict = {"time":[], "freeswitch":[], "plivo-cal":[], "plivo-rec":[], "plivo-eve":[], "s3upload":[], "voipmon":[], "redis-ser":[], "pcap-uploader":[]}
    mem_dict = {"time":[], "freeswitch":[], "plivo-cal":[], "plivo-rec":[], "plivo-eve":[], "s3upload":[], "voipmon":[], "redis-ser":[], "pcap-uploader":[]}
    line_num = 0
    line_count = len(file_lines)
    while (line_num < line_count):
        #Get the system level CPU and Mem
        if file_lines[line_num].startswith("top - "):
            time_load = file_lines[line_num].split()
            cpu_dict["time"].append(time_load[2])
            mem_dict["time"].append(time_load[2])

            cpu_data = file_lines[line_num+2].split()
            mem_data = file_lines[line_num+3].split()
            mem_data_cached = file_lines[line_num+4].split()

            actual_cpu_used = str("{0:.2f}".format(100.00 - float(cpu_data[7])))
            actual_mem_used = str(int(mem_data[4])-int(mem_data[8])-int(mem_data_cached[8]))

            concatinated_data = [time_load[2]] + \
                                [cpu_data[1], cpu_data[3], cpu_data[5], cpu_data[7], cpu_data[9], cpu_data[11], cpu_data[13], cpu_data[15]] + \
                                [mem_data[2], mem_data[4], mem_data[6], mem_data[8], mem_data_cached[8], actual_cpu_used, actual_mem_used] + \
                                [time_load[11]]

            system_level_usage.write(", ".join(concatinated_data))
            system_level_usage.write("\n")

            line_num = line_num + 5
        if "root" in file_lines[line_num] or "redis" in file_lines[line_num]:
            #Process level data
            data = file_lines[line_num].strip()
            cpu_usage = data.split()[8]
            mem_usage = data.split()[5]
            if data.endswith("freeswitch"):
                cpu_dict["freeswitch"].append(cpu_usage)
                mem_dict["freeswitch"].append(mem_usage)
            elif data.endswith("plivo-call+"):
                cpu_dict["plivo-cal"].append(cpu_usage)
                mem_dict["plivo-cal"].append(mem_usage)
            elif data.endswith("plivo-reco+"):
                cpu_dict["plivo-rec"].append(cpu_usage)
                mem_dict["plivo-rec"].append(mem_usage)
            elif data.endswith("plivo-event"):
                cpu_dict["plivo-eve"].append(cpu_usage)
                mem_dict["plivo-eve"].append(mem_usage)
            elif data.endswith("s3upload"):
                cpu_dict["s3upload"].append(cpu_usage)
                mem_dict["s3upload"].append(mem_usage)
            elif data.endswith("voipmonitor"):
                cpu_dict["voipmon"].append(cpu_usage)
                mem_dict["voipmon"].append(mem_usage)
            elif data.endswith("redis-serv+"):
                cpu_dict["redis-ser"].append(cpu_usage)
                mem_dict["redis-ser"].append(mem_usage)
            elif data.startswith("2547"):
                cpu_dict["pcap-uploader"].append(cpu_usage)
                mem_dict["pcap-uploader"].append(mem_usage)
            line_num = line_num + 1
        else:
            line_num = line_num + 1
    print(len(cpu_dict["time"]))
    print(len(cpu_dict["freeswitch"]))
    print(len(cpu_dict["plivo-cal"]))
    print(len(cpu_dict["plivo-rec"]))
    print(len(cpu_dict["plivo-eve"]))
    print(len(cpu_dict["s3upload"]))
    print(len(cpu_dict["voipmon"]))
    print(len(cpu_dict["redis-ser"]))
    print(len(cpu_dict["pcap-uploader"]))
    for i in range(len(cpu_dict["time"])):
        concatinated_data_cpu = [cpu_dict["time"][i], cpu_dict["freeswitch"][i], cpu_dict["plivo-cal"][i], cpu_dict["plivo-rec"][i], cpu_dict["plivo-eve"][i], cpu_dict["s3upload"][i], cpu_dict["voipmon"][i], cpu_dict["redis-ser"][i], cpu_dict["pcap-uploader"][i]]
        concatinated_data_mem = [mem_dict["time"][i], mem_dict["freeswitch"][i], mem_dict["plivo-cal"][i], mem_dict["plivo-rec"][i], mem_dict["plivo-eve"][i], mem_dict["s3upload"][i], mem_dict["voipmon"][i], mem_dict["redis-ser"][i], mem_dict["pcap-uploader"][i]]

        process_level_cpu_usage.write(", ".join(concatinated_data_cpu))
        process_level_cpu_usage.write("\n")
        process_level_mem_usage.write(", ".join(concatinated_data_mem))
        process_level_mem_usage.write("\n")
