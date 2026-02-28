//write a program to find the non repeating element in a String 

class Non{

    public static void main(String[] args) {
        {
            String stri = "ashithrai";
            for(int i=0;i<stri.length();i++){
                char c = stri.charAt(i);
                if(stri.indexOf(c) == stri.lastIndexOf(c)){
                    System.out.println("The non repeating element is: " + c);
                    break;
                }
            }
        }
    }

}
