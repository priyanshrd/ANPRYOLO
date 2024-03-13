#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIZE 100

// Structure to represent a stack
struct Stack
{
    int top;
    char items[MAX_SIZE];
};

// Function to initialize the stack
void initialize(struct Stack *stack)
{
    stack->top = -1;
}

// Function to check if the stack is full
int isFull(struct Stack *stack)
{
    return stack->top == MAX_SIZE - 1;
}

// Function to check if the stack is empty
int isEmpty(struct Stack *stack)
{
    return stack->top == -1;
}

// Function to push an item onto the stack
void push(struct Stack *stack, char value)
{
    if (isFull(stack))
    {
        printf("Stack Overflow\n");
        return;
    }
    stack->items[++stack->top] = value;
}

// Function to pop an item from the stack
char pop(struct Stack *stack)
{
    if (isEmpty(stack))
    {
        printf("Stack Underflow\n");
        exit(1);
    }
    return stack->items[stack->top--];
}

// Function to get the top element of the stack without removing it
char peek(struct Stack *stack)
{
    if (isEmpty(stack))
    {
        printf("Stack is empty\n");
        exit(1);
    }
    return stack->items[stack->top];
}

// Function to check if a character is an operator
int isOperator(char ch)
{
    return (ch == '+' || ch == '-' || ch == '*' || ch == '/');
}

// Function to return precedence of operators
int precedence(char op)
{
    if (op == '+' || op == '-')
        return 1;
    else if (op == '*' || op == '/')
        return 2;
    return 0;
}

// Function to convert infix expression to postfix expression
void infixToPostfix(char *infix, char *postfix)
{
    struct Stack stack;
    initialize(&stack);
    int i = 0, j = 0;

    while (infix[i] != '\0')
    {
        char current = infix[i];

        if (current == '(')
        {
            push(&stack, current);
        }
        else if (current == ')')
        {
            while (!isEmpty(&stack) && peek(&stack) != '(')
            {
                postfix[j++] = pop(&stack);
            }
            if (!isEmpty(&stack) && peek(&stack) == '(')
            {
                pop(&stack); // Discard '(' from stack
            }
            else
            {
                printf("Invalid expression: Mismatched parenthesis\n");
                return;
            }
        }
        else if (isOperator(current))
        {
            while (!isEmpty(&stack) && precedence(current) <= precedence(peek(&stack)))
            {
                postfix[j++] = pop(&stack);
            }
            push(&stack, current);
        }
        else
        {
            postfix[j++] = current;
        }
        i++;
    }

    while (!isEmpty(&stack))
    {
        if (peek(&stack) == '(')
        {
            printf("Invalid expression: Mismatched parenthesis\n");
            return;
        }
        postfix[j++] = pop(&stack);
    }
    postfix[j] = '\0';
}

int main()
{
    char infix[MAX_SIZE];
    char postfix[MAX_SIZE];

    printf("Enter infix expression: ");
    scanf("%s", infix);

    infixToPostfix(infix, postfix);

    printf("Postfix expression: %s\n", postfix);

    return 0;
}
