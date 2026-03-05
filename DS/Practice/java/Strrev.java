class Strrev{

    public static void main(String[] args) {
        {
            String s = "Hello";
            String right = "";
            for(int i = s.length() - 1; i >= 0; i--) {
                right = right + s.charAt(i);
            }
            System.out.println("Original: " + s);
            System.out.println("Reversed: " + right);
        }
    }
}