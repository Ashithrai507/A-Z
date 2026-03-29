class Reverse {
    public static void main(String[] args) {
        String arr1 = "hello";
        char[] arr = arr1.toCharArray();
        int left =0,right = arr.length-1;
        while(left<right)
        {
                char temp = arr[left];
                arr[left] = arr[right];
                arr[right] = temp;
                left ++;
                right --;
        }
        System.out.println(new String(arr));
    }
}