int get_max (int a[], int n){
   int max = a[0];
   for (int i = 1; i < n; i++)
      if (a[i] > max)
         max = a[i];
   return max;
}

void sort (int a[], int n){
   int bucket[10][10], bucket_cnt[10];
   int i, j, k, r, NOP = 0, divisor = 1, lar, pass;
   lar = get_max (a, n);
   while (lar > 0){
      NOP++;
      lar /= 10;
   }
   for (pass = 0; pass < NOP; pass++){
      for (i = 0; i < 10; i++){
         bucket_cnt[i] = 0;
      }
      for (i = 0; i < n; i++){
         r = (a[i] / divisor) % 10;
         bucket[r][bucket_cnt[r]] = a[i];
         bucket_cnt[r] += 1;
      }
      i = 0;
      for (k = 0; k < 10; k++){
         for (j = 0; j < bucket_cnt[k]; j++){
            a[i] = bucket[k][j];
            i++;
         }
      }
      divisor *= 10;
      printf ("After pass %d : ", pass + 1);
      for (i = 0; i < n; i++)
         printf ("%d ", a[i]);
      printf ("\n");
   }
}

int search(int a[], int beg, int end, int val)    
{    
    int mid;    
    if(end >= beg)     
    {        mid = (beg + end)/2;    
/* if the item to be searched is present at middle */  
        if(a[mid] == val)    
        {                 
            return mid+1;    
        }    
            /* if the item to be searched is smaller than middle, then it can only be in left subarray */  
        else if(a[mid] < val)     
        {  
            return search(a, mid+1, end, val);    
        }    
            /* if the item to be searched is greater than middle, then it can only be in right subarray */  
        else     
        {  
            return search(a, beg, mid-1, val);    
        }          
    }    
    return -1;     
} 
