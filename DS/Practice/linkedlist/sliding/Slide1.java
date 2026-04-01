package sliding;

public class Slide1 {
    public static void main(String[] args) {
    int arr[] = {1, 2, 5, 4, 2, 6, 4};
        int k = 2;
        int windowSum = 0;
        for (int i = 0; i < k; i++) {
            windowSum += arr[i];
        }
        System.out.println("Window [0,1] Sum: " + windowSum);
        for (int i = k; i < arr.length; i++) {
            windowSum += arr[i];       
            windowSum -= arr[i - k];  

            System.out.println("Window [" + (i - k + 1) + "," + i + "] Sum: " + windowSum);
        }
}
}

