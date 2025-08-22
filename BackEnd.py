import re

total_api_requests = 0
endpoint_popularity = {}
http_status_codes = {}
endpoint_response_times = {}
unique_user_ids = set()
user_batch_counts = {'2022': 0, '2023': 0, '2024': 0, '2025': 0}
timetable_strategy_usage = { 'backtracking': 0, 'iterative': 0}
total_timetables_generated = 0
generate_call_count = 0

f = open('timetable.log', 'r')
for line in f:
    api_match = re.search(r'(GET|POST)\s(/[\w_]+)\s(\d{3})\s([\d.]+)(ms|μs)', line)
    if api_match:
        http_method, endpoint, status_code, time_str, time_unit = api_match.groups()
        response_time = float(time_str)
        total_api_requests += 1
        endpoint_popularity[endpoint] = endpoint_popularity.get(endpoint, 0) + 1
        http_status_codes[status_code] = http_status_codes.get(status_code, 0) + 1
        if time_unit == 'μs':
            response_time /= 1000.0
        if endpoint not in endpoint_response_times:
            endpoint_response_times[endpoint] = []
        endpoint_response_times[endpoint].append(response_time)

    user_match = re.search(r'\[(2022|2023|2024|2025)[A-Z0-9]+\]', line)
    if user_match:
        full_id = user_match.group(0)
        year = user_match.group(1)
        unique_user_ids.add(full_id)
                        
    if 'Using Heuristic Backtracking Strategy' in line:
        timetable_strategy_usage['backtracking'] += 1
    elif 'Using Iterative Random Sampling Strategy' in line:
        timetable_strategy_usage['iterative'] += 1

    gen_complete_match = re.search(r'Generation Complete: Found (\d+) timetables', line)
    if gen_complete_match:
        timetables_found = int(gen_complete_match.group(1))
        total_timetables_generated += timetables_found
        generate_call_count += 1

print("\n--- Log File Analysis Report ---")
print("\nTraffic & Usage Analysis")
print("-" * 26)
print(f"Total API Requests Logged: {total_api_requests}")
print("\nEndpoint Popularity:")
for endpoint, count in sorted(endpoint_popularity.items(), key=lambda item: item[1], reverse=True):
    percentage = (count / total_api_requests) * 100 if total_api_requests > 0 else 0
    print(f"  {endpoint}: {count} requests ({percentage:.1f}%)")

print("\nHTTP Status Codes:")
for code, count in sorted(http_status_codes.items()):
    print(f"  - {code}: {count} times")

print("\nPerformance Metrics")
print("-" * 19)
for endpoint, times in sorted(endpoint_response_times.items()):
    if times:
        average_time = sum(times) / len(times)
        max_time = max(times)
        print(f"Endpoint: {endpoint}")
        print(f"  Average Response Time: {average_time:.2f} ms")
        print(f"  Max Response Time: {max_time:.2f} ms")

print("\nApplication-Specific Insights")
print("-" * 29)
print("Timetable Generation Strategy Usage:")
print(f"  Heuristic Backtracking: {timetable_strategy_usage['backtracking']} times")
print(f"  Iterative Random Sampling: {timetable_strategy_usage['iterative']} times")

avg_timetables = (total_timetables_generated / generate_call_count) if generate_call_count > 0 else 0
print(f"\nAverage Timetables Found per /generate call: {avg_timetables:.2f}")
print(f"Total number of timetables generated: {total_timetables_generated}")

print("\nUnique ID Analysis")
print("-" * 18)
print(f"Total Unique IDs found: {len(unique_user_ids)}")
for year in sorted(user_batch_counts.keys()):
    year_specific_ids = {uid for uid in unique_user_ids if uid.startswith(f"[{year}")}
    print(f"  Batch of {year}: {len(year_specific_ids)} unique IDs")
print("\n--- End of Report ---\n")



