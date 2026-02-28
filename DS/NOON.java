class NOON {
    public static void main(String[] args) {
        String s = "ashith";

        // Use a frequency table to find the first non-repeating character.
        int[] freq = new int[256]; // assumes standard ASCII; switch to Map<Character,Integer> for full Unicode
        for (int i = 0; i < s.length(); i++) {
            freq[s.charAt(i)]++;
        }

        boolean found = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (freq[c] == 1) {
                System.out.println("The non repeating element is: " + c);
                found = true;
                break;
            }
        }

        if (!found) {
            System.out.println("No non-repeating character found.");
        }
    }
}