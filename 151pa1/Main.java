import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Main {

    private final static int[] kValues = {1, 3, 5, 9, 15};
    private final static String[] fileNames = {
        "/Users/yuanboteng/Downloads/151pa1/src/pa1train.txt",
        "/Users/yuanboteng/Downloads/151pa1/src/pa1validate.txt",
        "/Users/yuanboteng/Downloads/151pa1/src/pa1test.txt",
        "/Users/yuanboteng/Downloads/151pa1/src/projection.txt"};

    private static List<double[]> trainingData = new LinkedList<>();
    private static List<double[]> validationData = new LinkedList<>();
    private static List<double[]> testData = new LinkedList<>();
    private static List<double[]> matrixP = new ArrayList<>();
    private static List<double[]> projectedTrainingData = new LinkedList<>();
    private static List<double[]> projectedValidationData = new LinkedList<>();
    private static List<double[]> projectedTestData = new LinkedList<>();

    public static void main(String[] args) {

        readVectors(trainingData, fileNames[0]);
        readVectors(validationData, fileNames[1]);
        readVectors(testData, fileNames[2]);
        readVectors(matrixP, fileNames[3]);

        for (int k : kValues) {
            System.out.println("k = " + k);
            System.out.println("training errors = " + countErrors(trainingData, k, 784, trainingData) / trainingData.size());
            System.out.println("validation errors = " + countErrors(validationData, k, 784, trainingData) / validationData.size());
            System.out.println("test errors = " + countErrors(testData, k, 784, trainingData) / testData.size());
            System.out.println("--------------------");
        }
        System.out.println(" ");

        double[][] P = new double[matrixP.size()][];
        for (int i = 0; i < matrixP.size(); i++) {
            P[i] = matrixP.get(i);
        }

        projection(projectedTrainingData, trainingData, P);
        projection(projectedValidationData, validationData, P);
        projection(projectedTestData, testData, P);

        for (int k : kValues) {
            System.out.println("k = " + k);
            System.out.println("Projected training errors = " + countErrors(projectedTrainingData, k, 20, projectedTrainingData) / projectedTrainingData.size());
            System.out.println("Projected validation errors = " + countErrors(projectedValidationData, k, 20, projectedTrainingData) / projectedValidationData.size());
            System.out.println("Projected test errors = " + countErrors(projectedTestData, k, 20, projectedTrainingData) / projectedTestData.size());
            System.out.println("--------------------");
        }
    }

    private static double calculateDist(double[] v1, double[] v2) {
        if (v1.length != v2.length) {
            return -1;
        }
        double dist = 0;
        for (int i = 0; i < v1.length; i++) {
            dist += (v1[i] - v2[i]) * (v1[i] - v2[i]);
        }
        return Math.sqrt(dist);
    }

    private static double countErrors(List<double[]> srcData, int k, int labelIndex, List<double[]> train){
        double numberOfErrors = 0;
        for (double [] src : srcData) {
            Predictor predictor = new Predictor(k);
            for (double [] trainData : train) {
                predictor.addNeighbor(new Neighbor(calculateDist(src, trainData), trainData[labelIndex]));
            }
            if (predictor.predictLabel() != src[labelIndex]) {
                numberOfErrors++;
            }
        }
        return numberOfErrors;
    }

    private static void readVectors(List<double[]> vectors, String fileName) {
        File file = new File(fileName);
        try {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String bufferLine;
            while ((bufferLine = reader.readLine()) != null) {
                String[] numbers = bufferLine.split(" ");
                double[] data = new double[numbers.length];
                for (int i = 0; i < numbers.length; i++) {
                    data[i] = Double.parseDouble(numbers[i]);
                }
                vectors.add(data);
            }

        } catch (IOException e){
            e.printStackTrace();
        }
    }

    private static void projection(List<double[]> projectedVectors, List<double[]> src, double[][] P) {
        for (double[] row : src) {
            double label = row[784];
            double[] data = Arrays.copyOf(row, row.length - 1);
            double[] newVector = new double[21];
            newVector[20] = label;
            for (int i = 0; i < newVector.length - 1; i++) {
                for (int j = 0; j < data.length - 1; j++) {
                    newVector[i] += data[j] * P[j][i];
                }
            }
            projectedVectors.add(newVector);
        }
    }
}

class Predictor {
    private int k;
    private PriorityQueue<Neighbor> neighbors;

    Predictor(int k) {
        this.k = k;
        neighbors = new PriorityQueue<>(new pqComparator());
    }

    void addNeighbor(Neighbor n) {
        if (neighbors.size() >= k) {
            if (n.dist <= neighbors.peek().dist) {
                neighbors.poll();
                neighbors.add(n);
            }
        } else {
            neighbors.add(n);
        }
    }

    double predictLabel() {
        double label = -1;
        if (neighbors.size() != k) {
            return label;
        }

        HashMap<Double, Integer> hashMap = new HashMap<>();

        for (Neighbor neighbor : neighbors) {
            if (hashMap.containsKey(neighbor.label)) {
                hashMap.put(neighbor.label, hashMap.get(neighbor.label) + 1);
            } else {
                hashMap.put(neighbor.label, 1);
            }
        }

        int maxCount = 0;

        for (Map.Entry<Double, Integer> entry : hashMap.entrySet()) {
            if (maxCount < entry.getValue()) {
                label = entry.getKey();
                maxCount = entry.getValue();
            }
        }

        return label;
    }
}

class Neighbor {
    double dist;
    double label;
    Neighbor (double dist, double label) {
        this.dist = dist;
        this.label = label;
    }
}

class pqComparator implements Comparator<Neighbor> {

    @Override
    public int compare(Neighbor o1, Neighbor o2) {
        if (o2.dist > o1.dist) {
            return 1;
        } else if (o2.dist < o1.dist) {
            return -1;
        } else {
            return 0;
        }
    }
}
