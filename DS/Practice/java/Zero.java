class Zero{
    public static void main(String[] args) {
        int arr[] = {1,0,0,3,5,0,6,0};
        int newar[] = new int[arr.length];
        int j = 0;

        for (int i = 0; i < arr.length; i++) {
            if (arr[i] >= 1) {
                newar[j] = arr[i]; 
                j++; 
            }
        }

        for (int i = 0; i < newar.length; i++) {
            System.out.print(newar[i]+" ");
        }
    }
}
