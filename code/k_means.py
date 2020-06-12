# implements k-means clustering algorithm

import random
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# k-means algorithm plus assigns all codewords to same cluster
def kmeans(vectors, words, codewords, K, maxIters):
    centers, assignments, old_centers, vector_terms = [], [], [], []
    minimums = []
    # precalculating terms for run time
    vector_terms = [dotProduct(v, v) for v in vectors]
    code_indexes = [words.index(i) for i in codewords if i in words]
    code_length = len(code_indexes)

    # randomly initialize centers
    for i in range(K):
        centers.append(random.choice(vectors))

    # alternate way to initialize centers, maximizing distance between
    # initializeCenters(vectors, centers, vector_terms, K)

    for x in range(maxIters):
        logging.info("Iteration #: " + str(x))
        minimums = []
        if centers == old_centers:
            break
        old_centers = centers.copy
        c_terms = [dotProduct(c, c) for c in centers]
        assignments = []
        code_distances = []
        code_sums = []

        # assigns all codewords to nearest centroid
        for n in range(code_length):
            code_distances.append([])
            for o in range(K):
                index = code_indexes[n]
                # euclidean distance measure
                code_distances[n].append(vector_terms[index] + c_terms[o] - (2 * dotProduct(vectors[index], centers[o])))
        for p in range(K):
            code_sums.append(sum(code_distances[q][p] for q in range(len(code_distances))))
        logging.info("Assigned codewords")
        code_minimum = min(code_sums)
        code_center = code_sums.index(code_minimum)

        # assigns non-codewords to centroid with minimum distance
        for y in range(len(vectors)):
            if words[y] not in codewords:
                distances = []
                for z in range(K):
                    distances.append(vector_terms[y] + c_terms[z] - (2 * dotProduct(vectors[y], centers[z])))
                minimum = min(distances)
                minimums.append(minimum)
                assignments.append(distances.index(minimum))
            else:
                assignments.append(code_center)
        logging.info("Assigned others")

        # recalculates centroids based on average distance
        for j in range(K):
            points = [vectors[q] for q in range(len(vectors)) if assignments[q] == j]
            base = [0] * len(vectors[0])
            pt = len(points)
            for p in points:
                increment(base, 1 / pt, p)
            centers[j] = base
        logging.info("Adjusted means")

    return (centers, assignments, sum(minimums))

# dotproduct helper
def dotProduct(d1, d2):
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1[i] * d2[i] for i in range(len(d2)))


# vector addition helper
def increment(d1, scale, d2):
    for f in range(len(d2)):
        d1[f] = d1[f] + d2[f] * scale


# initializes centers by maximum distance to previous centers
def initializeCenters(vectors, centers, vector_terms, K):
    centers.append(random.choice(vectors))
    distances = []
    for i in range(K-1):
        logging.info("Assigning Center #: " + str(i))
        c_terms = [dotProduct(c, c) for c in centers]
        for y in range(len(vectors)):
            last = len(centers)-1
            val = vector_terms[y] + c_terms[last] - (2 * dotProduct(vectors[y], centers[last]))
            if i == 0:
                distances.append(val)
            else:
                distances[y] += val
        maximum = distances.index(max(distances))
        distances[maximum] = float("-inf")
        centers.append(vectors[maximum])