import math
from collections import Counter

def euclidean_distance(point1, point2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

def knn_predict(k, training_data, name, input_point):
    distances = [(euclidean_distance(input_point, x), name) for x, name in zip(training_data, name)]
    sorted_distances = sorted(distances, key=lambda x: x[0])

    k_nearest_name = [name for _, name in sorted_distances[:k]]
    counter = Counter(k_nearest_name)
    prediction = counter.most_common(1)[0][0]
    print(prediction)
    
    return prediction, sorted_distances

# Exemple d'utilisation
training_data = [[1, 2], [2, 3], [3, 4], [4, 5]]
name = ['A', 'B', 'C', 'D']
input_point = [2, 3]

k_value = 3
prediction = knn_predict(k_value, training_data, name, input_point)
print(f'Prediction: {prediction}')

