public class Stock {
    public static void main(String[] args) {
        int arr[] = {10,1,5,6,7,1};
        int left =0, right = left + 1,buy = 0;
        int min = arr[0];
        for(int i=1;i<arr.length;i++)
        {
            if(arr[i]<min)
            {
                min = arr[i];
            }
        }
        while(right<arr.length)
        {
            if(arr[right]>arr[left])
            {
                buy = Math.max(buy, arr[right]-arr[left]);
            }
            else
            {
                left = right;
            }
            right++;
        }
        System.out.println(buy);
    }
    
}
