// Remove Duplicates from Sorted Array II
class Repe {

    public static void main(String[] args) {
        Repe r = new Repe();
        int[] nums = {1,1,3,3,3,4,4,4,4,5,5};
        System.out.println(r.removeDuplicates(nums));
    }

    public int removeDuplicates(int[] nums) {
        
        if(nums.length <= 2) 
            return nums.length;
        
        int i = 2; 
        
        for(int j = 2; j < nums.length; j++) { 
            
            if(nums[j] != nums[i - 2]) {
                nums[i] = nums[j];
                i++;
            }
        }
        
        return i;
    }
}