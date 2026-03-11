class Major{
    public static void main(String[] args){
        int nums[] = {3,2,3,4,4,4,4,4,4,5,5,5,5,5,5,5};
        for(int i=0;i<nums.length;i++)
        {
            int count = 0;
            for(int j=i;j<nums.length;j++)
            {
                if(nums[i] == nums[j])
                {
                    count++;
                }
            }
            if(count > nums.length/2)
            {
                System.out.println(nums[i]);
                break;
            }
        }
    }
}