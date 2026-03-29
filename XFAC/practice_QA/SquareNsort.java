
class SquareNsort {
    public static void main(String[] args) {
        int arr[] = {-7, -3, 2, 3, 11};
        int left = 0,right =arr.length-1,pos = arr.length-1;
        int[] result = new int[arr.length];
        while(left<=right)
        {
            if(Math.abs(arr[left])>Math.abs(arr[right]))
            {
                result[pos] = arr[left]*arr[left];
                left++;
            }   
            else
            {
                result[pos] = arr[right]*arr[right];
                right--;
            }
            pos--;
        }
        for(int i=0;i<result.length;i++)
        {
            System.out.println(result[i]);
        }
    }
}

