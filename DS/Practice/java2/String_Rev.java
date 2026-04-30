class String_Rev {

    public static void main(String[] args)
    {
        char str[] = {'h','e','l','l','o'};
        String rev = "";
        for (int i = str.length - 1; i >= 0; i--) {
            rev = rev + str[i];
        }
        System.out.println(rev);
    }
}