"""
Intelligent Traffic Congestion Prediction and Smart Route Recommendation
CSA1717 - Artificial Intelligence
Dataset : Traffic Prediction Dataset (Kaggle - hasibullahaman)
ML Algo : Decision Tree Classifier
Search : A* Search

HOW TO RUN IN GOOGLE COLAB:
1. Download the dataset from:
https://www.kaggle.com/datasets/hasibullahaman/traffic-prediction-dataset
(the file is usually named "TrafficTwoMonth.csv" or "Traffic.csv" - rename it to
TrafficDataset.csv, OR just change the filename in pd.read_csv below to match
whatever file you downloaded)
2. In Colab, click the folder icon on the left sidebar -> upload icon -> upload
the CSV you downloaded.
3. Run all cells (Runtime -> Run all). Take screenshots of each printed section.
"""

# =====================================================================
# CELL 1: Imports and file upload (Colab-specific)
# =====================================================================
import pandas as pd, numpy as np, time, heapq, math
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, precision_recall_fscore_support,
confusion_matrix, classification_report)

# If running in Colab, uncomment the next 3 lines to upload the CSV interactively:
# from google.colab import files
# uploaded = files.upload()
# csv_filename = list(uploaded.keys())[0]

csv_filename = 'TrafficDataset.csv' # <-- change this to your uploaded file's name

# =====================================================================
# CELL 2: SECTION 1 - Data loading and preprocessing
# =====================================================================
print("="*78)
print("SECTION 1: DATA LOADING AND PREPROCESSING")
print("="*78)

df = pd.read_csv(csv_filename)
print("Raw shape:", df.shape)
print(df.head())

# ---- Feature engineering ----
df['Time'] = pd.to_datetime(df['Time'], format='%I:%M:%S %p')
df['Hour'] = df['Time'].dt.hour
df['Minute'] = df['Time'].dt.minute

dow_map = {'Monday':0,'Tuesday':1,'Wednesday':2,'Thursday':3,
'Friday':4,'Saturday':5,'Sunday':6}
df['DayNum'] = df['Day of the week'].map(dow_map)
df['IsWeekend'] = df['DayNum'].isin([5,6]).astype(int)
df['IsPeak'] = df['Hour'].apply(lambda h: 1 if (7 <= h <= 10 or 16 <= h <= 20) else 0)

print("\nMissing values per column:")
print(df.isna().sum())

le = LabelEncoder()
df['TrafficSituationEnc'] = le.fit_transform(df['Traffic Situation'])
print("\nEncoded classes (alphabetical):", list(le.classes_))
print("\nClass distribution:")
print(df['Traffic Situation'].value_counts())

# =====================================================================
# CELL 3: SECTION 2 - Train/test split and Decision Tree training
# =====================================================================
print("\n" + "="*78)
print("SECTION 2: DECISION TREE MODEL TRAINING")
print("="*78)

FEATS = ['Hour','Minute','DayNum','IsWeekend','IsPeak',
'CarCount','BikeCount','BusCount','TruckCount','Total']
X = df[FEATS].values
y = df['TrafficSituationEnc'].values

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25,
random_state=42, stratify=y)
print(f"Train records: {len(Xtr)} Test records: {len(Xte)}")

t0 = time.time()
clf = DecisionTreeClassifier(max_depth=8, random_state=42)
clf.fit(Xtr, ytr)
train_time = time.time() - t0

t1 = time.time()
pred = clf.predict(Xte)
pred_time = (time.time() - t1) / len(Xte) * 1000

acc = accuracy_score(yte, pred)
pr, rc, f1, _ = precision_recall_fscore_support(yte, pred, average='macro')

print(f"\nAccuracy : {acc*100:.2f}%")
print(f"Macro Precision : {pr*100:.2f}%")
print(f"Macro Recall : {rc*100:.2f}%")
print(f"Macro F1-score : {f1*100:.2f}%")
print(f"Training time : {train_time:.4f} s")
print(f"Inference time : {pred_time:.4f} ms/sample")

print("\nConfusion Matrix (rows=actual, cols=predicted):")
cm = confusion_matrix(yte, pred)
print(pd.DataFrame(cm, index=le.classes_, columns=le.classes_))

print("\nClassification Report:")
print(classification_report(yte, pred, target_names=le.classes_))

fi = sorted(zip(FEATS, clf.feature_importances_), key=lambda t: -t[1])
print("Feature importance:")
for f, v in fi:
print(f" {f:12s} {v*100:6.2f}%")

# =====================================================================
# CELL 4: SECTION 3 - Road network graph and congestion-aware edge cost
# =====================================================================
print("\n" + "="*78)
print("SECTION 3: ROAD NETWORK GRAPH AND CONGESTION-AWARE EDGE COST")
print("="*78)

coords = {'A':(0,0), 'B':(2,1), 'C':(4,1), 'D':(6,0),
'E':(1,3), 'F':(3,3), 'G':(5,3), 'H':(6,4)}

# (u, v, length_km, base_car, base_bike, base_bus, base_truck, peak_sensitivity)
edges_raw = [
('A','B',2.0, 55, 9,4,7, 3.0), # arterial - very peak-sensitive
('A','E',2.5, 20, 5,1,3, 1.1), # local - mild peak sensitivity
('B','C',2.2, 60,10,5,8, 3.2), # arterial - very peak-sensitive
('B','F',2.4, 25, 6,2,4, 1.3), # collector - mild
('C','D',2.1, 58,10,4,7, 3.1), # arterial
('C','G',2.3, 24, 6,2,4, 1.2), # collector
('D','H',2.6, 22, 5,2,4, 1.2), # collector
('E','F',2.0, 18, 4,1,3, 1.0), # local
('F','G',2.1, 26, 6,2,4, 1.3), # collector
('G','H',2.2, 24, 6,2,4, 1.2), # collector
]

graph = {}
for u, v, d, c, bk, bu, tr, sens in edges_raw:
graph.setdefault(u, []).append((v, d, c, bk, bu, tr, sens))
graph.setdefault(v, []).append((u, d, c, bk, bu, tr, sens))

FREE_SPEED = 45.0 # km/h, free-flow speed assumed uniform for this local network
PENALTY = {'low': 1.0, 'normal': 1.3, 'high': 1.8, 'heavy': 2.6}

def predict_edge_level(car, bike, bus, truck, hour, dow, sens=1.0):
is_wk = 1 if dow >= 5 else 0
is_pk = 1 if (7 <= hour <= 10 or 16 <= hour <= 20) else 0
mult = 1.0 + (sens - 1.0) * is_pk * (0.6 if is_wk else 1.0)
car, bike, bus, truck = car*mult, bike*mult, bus*mult, truck*mult
total = car + bike + bus + truck
x = np.array([[hour, 0, dow, is_wk, is_pk, car, bike, bus, truck, total]])
level_idx = clf.predict(x)[0]
return le.inverse_transform([level_idx])[0]

def edge_cost(u, v, d, car, bike, bus, truck, hour, dow, sens=1.0):
level = predict_edge_level(car, bike, bus, truck, hour, dow, sens)
time_min = d / (FREE_SPEED / PENALTY[level]) * 60.0
return time_min, level

def h_euclidean(n, goal, vmax=FREE_SPEED):
(x1, y1), (x2, y2) = coords[n], coords[goal]
return math.hypot(x1 - x2, y1 - y2) / vmax * 60.0

print(f"Nodes: {len(coords)} Edges: {len(edges_raw)}")
for u, v, d, c, bk, bu, tr, sens in edges_raw:
print(f" {u}-{v} length={d:.1f}km base_profile(car,bike,bus,truck)="
f"({c},{bk},{bu},{tr}) peak_sensitivity={sens}")

# =====================================================================
# CELL 5: SECTION 4 - A* Search and the distance-only baseline
# =====================================================================
def astar(src, dst, hour, dow):
open_heap = [(h_euclidean(src, dst), 0.0, src, [src])]
gscore = {src: 0.0}
expanded = 0
levels_used = {}
while open_heap:
f, g, n, path = heapq.heappop(open_heap)
expanded += 1
if n == dst:
return path, g, expanded, levels_used
for v, d, c, bk, bu, tr, sens in graph[n]:
cost, level = edge_cost(n, v, d, c, bk, bu, tr, hour, dow, sens)
levels_used[(n, v)] = level
ng = g + cost
if ng < gscore.get(v, float('inf')):
gscore[v] = ng
heapq.heappush(open_heap, (ng + h_euclidean(v, dst), ng, v, path + [v]))
return None, float('inf'), expanded, levels_used

def shortest_distance_route(src, dst):
open_heap = [(0.0, src, [src])]
dist = {src: 0.0}
while open_heap:
d, n, path = heapq.heappop(open_heap)
if n == dst:
return path, d
for v, dd, c, bk, bu, tr, sens in graph[n]:
nd = d + dd
if nd < dist.get(v, 1e9):
dist[v] = nd
heapq.heappush(open_heap, (nd, v, path + [v]))
return None, float('inf')

def route_time(path, hour, dow):
t = 0.0
for a, b in zip(path, path[1:]):
for v, d, c, bk, bu, tr, sens in graph[a]:
if v == b:
cost, _ = edge_cost(a, b, d, c, bk, bu, tr, hour, dow, sens)
t += cost
break
return t

# =====================================================================
# CELL 6: SECTION 5 - Test cases: congestion-aware route recommendation
# =====================================================================
print("\n" + "="*78)
print("SECTION 4: TEST CASES - CONGESTION-AWARE ROUTE RECOMMENDATION (A*)")
print("="*78)

TCS = [
dict(id='TC1', src='A', dst='H', hour=2, dow=1, desc='Off-peak, early morning (Tuesday 2 AM)'),
dict(id='TC2', src='A', dst='H', hour=9, dow=1, desc='Morning peak (Tuesday 9 AM)'),
dict(id='TC3', src='A', dst='H', hour=18, dow=4, desc='Evening peak (Friday 6 PM)'),
dict(id='TC4', src='A', dst='G', hour=9, dow=1, desc='Morning peak, shorter trip A->G'),
dict(id='TC5', src='B', dst='H', hour=14, dow=6, desc='Weekend midday (Sunday 2 PM)'),
]

summary = []
for tc in TCS:
t0 = time.perf_counter()
path, cost, exp, levels = astar(tc['src'], tc['dst'], tc['hour'], tc['dow'])
ta = (time.perf_counter() - t0) * 1000
sp, skm = shortest_distance_route(tc['src'], tc['dst'])
st = route_time(sp, tc['hour'], tc['dow'])
saved = st - cost
saved_pct = (saved / st * 100) if st > 0 else 0

print(f"\n[{tc['id']}] {tc['src']} -> {tc['dst']} | {tc['desc']} "
      f"(hour={tc['hour']}, dow={tc['dow']})")
print(f"  A\* recommended route : {'->'.join(path):15s} ETA={cost:6.2f} min  "
      f"nodes\_expanded={exp}  runtime={ta:.3f} ms")
print(f"  Distance-only route  : {'->'.join(sp):15s} ETA={st:6.2f} min  "
      f"({skm:.1f} km, congestion-unaware)")
print(f"  Time saved by A\* vs distance-only baseline: {saved:5.2f} min ({saved\_pct:5.2f}%)")

summary.append(dict(id=tc['id'], a\_star=cost, base=st, saved\_pct=saved\_pct,
                     exp=exp, ta=ta))

print("\n" + "="*78)
print("SECTION 5: AGGREGATE COMPARISON")
print("="*78)
print(f"{'TC':5s}{'A* ETA':>10s}{'Baseline ETA':>14s}{'Saved %':>10s}"
f"{'Nodes exp':>11s}{'Runtime ms':>12s}")
for s in summary:
print(f"{s['id']:5s}{s['a_star']:10.2f}{s['base']:14.2f}{s['saved_pct']:10.2f}"
f"{s['exp']:11d}{s['ta']:12.3f}")

print(f"\nMean travel-time saving vs distance-only routing: "
f"{np.mean([s['saved_pct'] for s in summary]):.2f}%")
print(f"Mean nodes expanded: {np.mean([s['exp'] for s in summary]):.1f} "
f"Mean runtime: {np.mean([s['ta'] for s in summary]):.3f} ms")

# =====================================================================
# CELL 7: SECTION 6 - PySpark-style RDD aggregation (map / reduceByKey)
# =====================================================================
print("\n" + "="*78)
print("SECTION 6: PYSPARK-STYLE RDD AGGREGATION (map / reduceByKey)")
print("="*78)

rdd = list(df[['Hour', 'Total']].itertuples(index=False, name=None))
mapped = [(int(h), (t, 1)) for h, t in rdd]
agg = {}
for k, (t, c) in mapped:
s = agg.get(k, (0.0, 0))
agg[k] = (s[0] + t, s[1] + c)

print(f"{'Hour':>5s}{'Mean Total vehicles':>22s}{'Samples':>10s}{'Peak?':>8s}")
for h in sorted(agg):
s, c = agg[h]
print(f"{h:5d}{s/c:22.2f}{c:10d}{('YES' if (7<=h<=10 or 16<=h<=20) else '-'):>8s}")

print("\nDone.")
