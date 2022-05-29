#include<stdio.h>
#include"sortnsearch.h"
int main(){
int a[10], s;
int n = sizeof(a) / sizeof(a[0]); // size of array  
for(int i = 0; i < 10; i++){
	printf("Enter a number: ");
	scanf("%d", &a[i]);	
	}
sort(a, 10);
for(int i = 0; i < 10; i++){
	printf("%d\t", a[i]);	
	}

printf("\nEnter element to search: ");
scanf("%d", &s);

int res = search(a, 0, n-1, s); // Store result
 if (res == -1)  
  printf("\nElement is not present in the array");  
  else  
  printf("\nElement is present at %d position of array", res);    
return 0;
}
