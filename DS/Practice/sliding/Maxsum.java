public class Maxsum {
    public static void main(String[] args) {
        int arr[] = {2,1,5,1,3,2};
        int k=3;
        int cs = 0;
        for(int i=0;i<k;i++)
        {
            cs = cs + arr[i];
        }
        int max = cs;
        for(int i=k;i<arr.length;i++)
        {
            cs = cs + arr[i] - arr[i-k];
            if(cs > max)
            {
                max = cs;
            }
        }
        
        System.out.println(max);
    }
}
