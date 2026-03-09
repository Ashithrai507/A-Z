class Dupz { 
    public static void main(String[] args) { 
        int arr[] = {1, 0, 2, 3, 0, 4, 5, 0}; 
        int newa[] = new int[arr.length]; 
        int k = 0; 

        for (int i = 0; i < arr.length && k < arr.length; i++) {
            newa[k] = arr[i];
            k++;
            if (arr[i] == 0 && k < arr.length) {
                newa[k] = 0;
                k++;
            }
        }
        
        for(int i=0;i<newa.length;i++)
        {
            System.out.println(newa[i]);
        }
    } 
}
