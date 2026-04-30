class Wind {

    public static void main(String[] args) {
        String S = "10212";
        int last0 = -1;
        int last1 = -1;
        int last2 = -1;
        int minLength = Integer.MAX_VALUE;

        for(int i=0;i<S.length();i++){
            char c = S.charAt(i);
            if(c=='0') last0 = i;
            else if(c=='1')last1 = i;
            else if(c=='2')last2 = i;
            
            if (last0 != -1 && last1 != -1 && last2 != -1) {
                int start = Math.min(last0, Math.min(last1, last2));
                minLength = Math.min(minLength, currentLength);
            }
        }
        
        System.out.println(minLength == Integer.MAX_VALUE ? -1 : minLength);
    }
}