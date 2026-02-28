class TwoSum {

    public static void main(String[] args)
    {
        int[] num = {10,20,35,50};
        int target = 40;
        boolean flag = false;
        
        for(int i=0;i<num.length;i++)
        {
            for(int j=i+1;j<num.length;j++)
            {
                
                if(num[i] + num[j]==target)
                {
                    System.out.println("true");
                    flag = true;
                    break;
                }
            if(flag)
            {
                break;
            }
            }
        }
        if(!flag)
        {
            System.out.println("false");
        }
    }
}