import java.util.Scanner;
class Llink3 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n=0;
        
        System.out.println("enter the number of nodes");
        n = sc.nextInt();
        
        System.out.println("enter the first node");
        Node head = new Node(sc.nextInt());
        Node current = head;
        
        for(int i=0;i<n-1;i++)
        {
            System.out.print("Enter next value: ");
            int val = sc.nextInt();
            
            current.next = new Node(val);
            
            current = current.next;
        }
        Node temp = head;
        while (temp != null) {
            System.out.print(temp.data + " -> ");
            temp = temp.next;
        }
        System.out.println("null");
        sc.close();
        
        
       
    }
}
class Node{
    int data;
    Node next;
    
    Node(int d){
        data = d;
        next = null;
    }
}