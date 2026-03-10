class Valid2{
    public static void main(String[] args){
        String arr = "A man a plan a canal Panama";
        char[] ch = arr.toCharArray();
        int left = 0;
        int right = ch.length - 1;
        while(left < right)
        {
                    ch[left] ^= ch[right];
                    ch[right] ^= ch[left];
                    ch[left] ^= ch[right];
                    left++;
                    right--;
                
        }

        System.out.println(ch);
    }
}