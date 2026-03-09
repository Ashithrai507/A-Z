class Rev1 {
    public static void main(String[] args) {
        long x = 1534236469; 
        int digit = 0, rev = 0;
        while (x != 0) {
            digit = (int)(x % 10);
            rev = rev * 10 + digit;
            x /= 10;
        }
        System.out.println(rev);
    }
}