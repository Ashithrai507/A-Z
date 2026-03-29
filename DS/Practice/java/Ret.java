public class Ret {
    public static void main(String[] args) {
        int nums[] = {1,2,4,1,2,1};
        int count = 0;
        for(int i=0;i<nums.length;i++)
        {
            
            for(int j=0;j<nums.length;j++)
            {
                if(nums[i]==nums[j])
                {
                    count ++;
                }
            }
             if(count<=1)
        {
            System.out.println("true");
        }
        else{
            System.out.println("false");
        }
        }
       
    }
}
