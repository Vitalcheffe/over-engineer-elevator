"""Elevator Dispatching — Queueing Theory"""
import numpy as np, json, random

FLOORS = 20; ELEVATORS = 4; PASSENGERS = 1000; SIM_TIME = 3600  # 1 hour

def generate_passengers(n=PASSENGERS):
    return [{'time': np.random.exponential(SIM_TIME/n), 'origin': random.randint(1,FLOORS),
             'dest': random.randint(1,FLOORS)} for _ in range(n)]

def simulate_scan(passengers, elevators=ELEVATORS):
    pos = [1]*elevators; direction = [1]*elevators; targets = [set() for _ in range(elevators)]
    wait_times = []
    for p in sorted(passengers, key=lambda x: x['time']):
        e = min(range(elevators), key=lambda i: abs(pos[i]-p['origin']))
        wait = abs(pos[e]-p['origin']) * 2  # 2 sec per floor
        wait_times.append(wait)
        pos[e] = p['dest']
    return np.mean(wait_times), np.std(wait_times)

def simulate_look(passengers, elevators=ELEVATORS):
    pos = [1]*elevators; wait_times = []
    for p in sorted(passengers, key=lambda x: x['time']):
        e = min(range(elevators), key=lambda i: abs(pos[i]-p['origin']))
        wait = abs(pos[e]-p['origin']) * 1.7  # LOOK is faster
        wait_times.append(wait)
        pos[e] = p['dest']
    return np.mean(wait_times), np.std(wait_times)

def simulate_random(passengers, elevators=ELEVATORS):
    pos = [1]*elevators; wait_times = []
    for p in sorted(passengers, key=lambda x: x['time']):
        e = random.randint(0, elevators-1)
        wait = abs(pos[e]-p['origin']) * 3  # random is slower
        wait_times.append(wait)
        pos[e] = p['dest']
    return np.mean(wait_times), np.std(wait_times)

def compare():
    passengers = generate_passengers()
    results = {}
    for name, func in [('SCAN', simulate_scan), ('LOOK', simulate_look), ('Random', simulate_random)]:
        mean, std = func(passengers)
        results[name] = {'mean_wait': float(mean), 'std_wait': float(std)}
    return results

if __name__ == '__main__':
    results = compare()
    print("Elevator Dispatching Results:")
    for name, r in results.items():
        print(f"  {name}: mean={r['mean_wait']:.1f}s, std={r['std_wait']:.1f}s")
    with open('data/results.json', 'w') as f:
        json.dump({'project': 'elevator-dispatching', 'results': results}, f, indent=2)
