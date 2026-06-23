class Solution {
    char[] stack;
    int top;
    public boolean isValid(String s) {
        int n = s.length();
        stack = new char[n];
        top = -1;
        for(int i=0;i<n;i++)
        {
            char ch = s.charAt(i);
        if(ch == '(' || ch == '{' || ch == '[')
        {
            push(ch);
        }
        else if(ch == ')' || ch == '}' || ch == ']')
        {
            if(top == -1)
            {
                return false;
            }
            char openBracket = pop();

             if ((ch == ')' && openBracket != '(') ||
                    (ch == '}' && openBracket != '{') ||
                    (ch == ']' && openBracket != '[')) {
                    return false; 
        }
        }
        }
        return (top == -1);
    }

    void push(char x)
    {
        if(top>=stack.length-1)
        {
            return ;
        }
        else{
            top++;
            stack[top] = x;
        }

    }
    char pop()
    {
        if(top == -1)
        {
            return '\0';
        }
        else{
            char value = stack[top];
            top--;
            return value;
        }
    }
}