
class Main {
    public static void main(String[] args) {
        Node head = new Node(2);
        head.next = new Node(2);
        head.next.next = new Node(3);
        head.next.next.next = new Node(3);
        
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        
        Node prev = null;
        Node current = head;
        while (current != null) {
            Node nextTemp = current.next;
            current.next = prev;
            prev = current;
            current = nextTemp;
        }
        head = prev;
        current = head;
        while(current != null)
        {
            System.out.println(current.data);
            current = current.next;
        }
        
        
    }
}

class Node {
    int data;
    Node next;
    
    Node(int d){
        data = d;
        next = null;
    }
}