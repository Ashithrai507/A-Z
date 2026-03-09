class Subs {
    public static void main(String[] args) {
        String input = "my name is ashith";
        String result = "";
        String currentWord = "";

        for (int i = 0; i < input.length(); i++) {
            char ch = input.charAt(i);

            if (ch != ' ') {
                currentWord = ch + currentWord;
            } else {
                result += currentWord + " ";
                currentWord = ""; 
            }
        }
        result += currentWord;

        System.out.println(result);
    }
}
