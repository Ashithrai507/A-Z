class DupII {

    public static void main(String[] ashith)
    {
        int nums[] =  {1,1,1,2,2,3};
        int newarr[] = new int[nums.length];
        int left = 0,count = 0;
        int right = nums.length -1;
        while(left < right)
        {
            if(left == right)
            {
                count++;
                if(count > 2)
                {
                    break;
                }
                newarr[left] = nums[left];
                break;
            }
        }
            for(int i=0;i<newarr.length;i++)
            {
                System.out.println(newarr[i]);
            }
    }
}