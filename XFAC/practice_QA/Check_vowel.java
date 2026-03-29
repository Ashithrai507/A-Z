class Check_vowel {
    public static void main(String[] args) {
        String arr1 = "hello";
        char[] arr = arr1.toCharArray();
        int left =0,right = arr.length-1;
        while(left<right)
        {
            if(!isVowel(arr[left]))
            {
                left++;
            }
            else if(!isVowel(arr[right]))
            {
                right++;
            }
            else
            {
                char temp = arr[left];
                arr[left] = arr[right];
                arr[right] = temp;
                left ++;
                right --;
            }
        }
        System.out.println(new String(arr));
    }
    public static boolean isVowel(char c) {
        c = Character.toLowerCase(c);
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
    }
}