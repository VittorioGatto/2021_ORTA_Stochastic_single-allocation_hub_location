#include <stdio.h>
#include <stdlib.h>

#define N_ROWS   5              /* number of y subdivisions */

typedef struct{
  int i;                        /* index in original */
  int new_i;                    /* new index */
  double x,y;
} coordinate;

int y_compare(const void *a, const void *b)
/* This function is used to sort coordinates by their y values */
{ if(((coordinate *) a)->y < ((coordinate *) b)->y) return -1;
  if(((coordinate *) a)->y > ((coordinate *) b)->y) return 1;
  if(((coordinate *) a)->x < ((coordinate *) b)->x) return -1;
  if(((coordinate *) a)->x > ((coordinate *) b)->x) return 1;
  fprintf(stderr,"ERROR: Two nodes at same location\n");
  exit(1);
}


int x_compare(const void *a, const void *b)
/* This functions is used to sort coordinates by their x values */
{ if(((coordinate *) a)->x < ((coordinate *) b)->x) return -1;
  if(((coordinate *) a)->x > ((coordinate *) b)->x) return 1;
  if(((coordinate *) a)->y < ((coordinate *) b)->y) return -1;
  if(((coordinate *) a)->y > ((coordinate *) b)->y) return 1;
  fprintf(stderr,"ERROR: Two nodes at same location\n");
  exit(1);
}

void main(int argc,char **argv)
{ int nn,np,p,q,r,NN;
  FILE *in=stdin;
  coordinate *pts;
  double **w,*OD; /* w[p][q]=Flow p to q, OD[p]=Total flow into & out of p */
  double collect,transfer,distribute; /* costs */
  int step,row_end,row_start,row_step,row_remainder;
  int n_cols,col_step,col_remainder,col_start,col_end;
  double *new_x,*new_y,**new_w, *new_OD;

  /*********************** Process Arguments ******************************/
  if(argc != 3){
    fprintf(stderr,
            "This program generates smaller hub location problems from a"
            "larger data set\nby combining nodes in a consistent manner\n"
            "USAGE: %s n p < input > output  \n"
            "\t n      Number of nodes for new problem\n"
            "\t p      Number of hubs for new problem\n"
            "\t input  Original data file\n"
            "\t output Data file for new problem\n"
            "Note: n should be a multiple of 5 and a divisor of 200\n",
            argv[0]);
    exit(1);
  }
  nn = atoi(argv[1]);           /* number of nodes */
  np = atoi(argv[2]);           /* number of hubs */
  if(nn <= np || nn <= 0 || np <=0){
    fprintf(stderr,"ERROR: Incorrect problem parameters\n");
    exit(1);
  }
  if(nn%N_ROWS != 0){
    fprintf(stderr,"ERROR: Number of nodes must be a multiple of %d\n",N_ROWS);
    exit(1);
  }
  
  /******************** Read data file *********************************/
  fscanf(in,"%d ",&NN); /* read in number of nodes & skip hub number */
  if(NN != 200)
     fprintf(stderr,"WARNING: Input is not the standard data file of AP problems\n");
  pts = (coordinate *)malloc((NN)*sizeof(coordinate));
  for(p=0;p<NN;p++){
    if(fscanf(in,"%lf %lf",&pts[p].x,&pts[p].y) != 2){
      fprintf(stderr,"ERROR: Can't read coordinates\n");
      exit(1);
    }
    pts[p].i = p;
  }
  w = (double * *)malloc((NN)*sizeof(double *));
  OD = (double *)malloc((NN)*sizeof(double));
  for(p=0;p<NN;p++) OD[p] = 0;
  for(p=0;p<NN;p++){            /* read flow matrix */
    w[p] = (double *)malloc((NN)*sizeof(double));
    for(q=0;q<NN;q++){
      if(fscanf(in,"%lf",&w[p][q]) != 1){
		fprintf(stderr,"ERROR: Can't read flow matrix\n");
		exit(1);
	  }
      OD[p] += w[p][q];
      OD[q] += w[p][q];
    }
  }
  fscanf(in,"%d %lf %lf %lf",&p,&collect,&transfer,&distribute);
  if(p != 8)
	fprintf(stderr,"WARNING: Input is not standard APdata200 file\n");
  /* fclose(in); */ /* no need to close */

  /************** Divide area into boxes with equal number of nodes *********/
  qsort(pts,NN,sizeof(coordinate),&y_compare);   /* Sort by y coordinate */
  n_cols = (nn/N_ROWS); /* number of columns (boxes in each row) */
  row_step = NN/N_ROWS;         /* number of nodes per row */
  row_start = 0;
  for(p=0;p<N_ROWS;p++){
    row_end = row_start + row_step;
    if(p < NN%N_ROWS) row_end++; /* Left over nodes in the first few rows */
    /* Sort row by x coordinates  */
    qsort(&pts[row_start],row_end-row_start,sizeof(coordinate),&x_compare);
    col_step = (row_end-row_start)/n_cols;  /* number of nodes per box */
    col_start = row_start;
    for(q=0;q<n_cols;q++){
      col_end = col_start + col_step;
      if(q < (row_end-row_start)%n_cols)
        col_end++;              /* put left over nodes in first few columns */
      for(r=col_start;r<col_end;r++){
        pts[r].new_i = p*n_cols + q; /* boxes are numbered across and down */
      }
      col_start = col_end;
    }
    row_start = row_end;
  }

  /******************* Calculate New Parameters ************************/
  new_x = (double *)malloc((nn)*sizeof(double));
  new_y = (double *)malloc((nn)*sizeof(double));
  new_w = (double**)malloc((nn)*sizeof(double*));
  new_OD = (double *)malloc((nn)*sizeof(double));
  for(p=0;p<nn;p++){            /* initialise to zero */
    new_x[p] = new_y[p] = new_OD[p] = 0;
    new_w[p] = (double *)malloc((nn)*sizeof(double));
    for(q=0;q<nn;q++) new_w[p][q] = 0;
  }
  for(p=0;p<NN;p++){
    new_x[pts[p].new_i] += OD[pts[p].i]*pts[p].x;
    new_y[pts[p].new_i] += OD[pts[p].i]*pts[p].y;
    new_OD[pts[p].new_i] += OD[pts[p].i];
    for(q=0;q<NN;q++)
      new_w[pts[p].new_i][pts[q].new_i] += w[pts[p].i][pts[q].i];   
  }
  for(p=0;p<nn;p++){    /* new coordinates are weighted average of the old */
    new_x[p] /= new_OD[p];
    new_y[p] /= new_OD[p];
  }

  /******************** Write out new problem ***************************/
  printf("%d\n",nn);            /* write number of nodes */
  for(p=0;p<nn;p++)             /* write coordinates */
    printf("%f %f\n",new_x[p],new_y[p]);
  for(p=0;p<nn;p++)             /* write flow matrix */
    for(q=0;q<nn;q++)
      printf("%f%c",new_w[p][q],((q==nn-1) ? '\n' : ' '));
  /* number of hubs, and costs per unit distance */
  printf("%d\n%f\n%f\n%f\n",np,collect,transfer,distribute);
}
