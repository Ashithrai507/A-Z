class Valid{
    public static void main(String[] args){
        String s = "OP";
        String newarr = "";
        String rev = "";
        for(int i=s.length() - 1; i>=0; i--) {
            if(s.charAt(i)>=65 && s.charAt(i)<=90 || s.charAt(i)>=97 && s.charAt(i)<=122)
            {
                rev += s.charAt(i);
            }
        }
        for(int i=0; i<s.length(); i++) {
            if(s.charAt(i)>=65 && s.charAt(i)<=90 || s.charAt(i)>=97 && s.charAt(i)<=122)
            {
                newarr += s.charAt(i);
            }
        }
        if(newarr.equalsIgnoreCase(rev)) {
            System.out.println("Palindrome");
        }
        else {
            System.out.println("Not a Palindrome");
        }
    }
}