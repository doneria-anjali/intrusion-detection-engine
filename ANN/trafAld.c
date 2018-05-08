#include <stdio.h>
#include <string.h>

#define MaxCon 800000
#define MaxLine 800
#define MaxToken 20

char input[MaxCon][MaxLine];
int inputCount;

int main(int argc, char **argv)
{
	FILE *finput, *ftrafAld;
	int i,j;
	char filename[MaxLine];
	int counter;
	int counter2, counter100;
	char line[MaxLine];	
	
	//Current connection data
	char line1[MaxLine];
	int connNum1;
	char tstamp1s[MaxToken];
	int tstamp1, tstamp12;
	int orig_p1,resp_p1;
	char orig_h1[MaxToken], resp_h1[MaxToken];
	char duration1[MaxToken], protocol1[MaxToken], service1[MaxToken], flag1[MaxToken];
	
	//Previous connection data
	char line2[MaxLine];
	int connNum2;
	char tstamp2s[MaxToken];
	int tstamp2, tstamp22;
	int orig_p2,resp_p2;
	char orig_h2[MaxToken], resp_h2[MaxToken];
	char duration2[MaxToken], protocol2[MaxToken], service2[MaxToken], flag2[MaxToken];
	int sentinel;
	
	//traffic related variables
	int count,srv_count,serror,rerror,same_srv,diff_srv,srv_serror,srv_error,srv_diff_host;
	int same_src_port;
	float serror_rate,srv_serror_rate,rerror_rate,srv_error_rate,same_srv_rate,diff_srv_rate,srv_diff_host_rate;
	float srv_rerror_rate,same_src_port_rate;

	if (argc != 2){
	  printf("Pass one file name!");
		return(1);
	}

  //Read and save input list
  sprintf(filename, "%s", argv[1]);
  finput = fopen(filename, "r");
  inputCount = 0;
  while(!feof(finput)){
  	fgets(line2, MaxLine, finput);
   	line2[strlen(line2)-1] = '\0';
    strcpy(input[inputCount],line2);
    inputCount = inputCount + 1;
  }
  fclose(finput);
  inputCount = inputCount - 1;

	//Calculate traffic variables
	counter2=0;
	for(counter=0; counter<inputCount; counter++){
		strcpy(line1, input[counter]);
		sscanf(line1, "%d %s %d %d %s %s %s %s %s %s %s",
                   &connNum1,&tstamp1s,&orig_p1,&resp_p1,&orig_h1,&resp_h1,
                   &duration1,&protocol1,&service1,&flag1);
		sscanf(tstamp1s, "%d.%d", &tstamp1, &tstamp12);
		orig_h1[strlen(orig_h1)] = '\0';
		resp_h1[strlen(resp_h1)] = '\0';
		service1[strlen(service1)] = '\0';
		flag1[strlen(flag1)] = '\0';
		
		//2 second connections
		sentinel=0;
		count=0;
		serror=0;
		rerror=0;
		same_srv=0;
		diff_srv=0;
		srv_count=0;
		srv_serror=0;
		srv_error=0;
		srv_diff_host=0;
		for(j=counter2; j<counter; j++){
			strcpy(line2, input[j]);
			sscanf(line2, "%d %s %d %d %s %s %s %s %s %s %s",
			      		&connNum2,&tstamp2s,&orig_p2,&resp_p2,&orig_h2,&resp_h2,
					&duration2,&protocol2,&service2,&flag2);
			sscanf(tstamp2s, "%d.%d", &tstamp2, &tstamp22);
			orig_h2[strlen(orig_h2)] = '\0';
			resp_h2[strlen(resp_h2)] = '\0';
			service2[strlen(service2)] = '\0';
			flag2[strlen(flag2)] = '\0';
			if((tstamp1-2)<=tstamp2 && tstamp2<=tstamp1){
				if(sentinel==0){ 
					counter2=j;
					sentinel=1;
				}
				if (strcmp(resp_h1,resp_h2)==0){
					count= count + 1;
					if (strcmp(flag2,"S0")==0 || strcmp(flag2,"S1")==0 || strcmp(flag2,"S2")==0 || strcmp(flag2,"S3")==0){
						serror= serror + 1;
					}
					if (strcmp(flag2,"REJ")==0){
						rerror= rerror + 1;
					}
					if (strcmp(service2,"other")!=0 && strcmp(service1,service2)==0){
						same_srv= same_srv + 1;
					}
					if (strcmp(service1,service2)!=0){
						diff_srv= diff_srv + 1;
					}	
				}
				if (resp_p1==resp_p2){
					srv_count= srv_count + 1;
					if (strcmp(flag2,"S0")==0 || strcmp(flag2,"S1")==0 || strcmp(flag2,"S2")==0 || strcmp(flag2,"S3")==0){
						srv_serror= srv_serror + 1;
					}
					if (strcmp(flag2,"REJ")==0){
						srv_error= srv_error + 1;
					}
					if (strcmp(resp_h1,resp_h2)!=0){
						srv_diff_host= srv_diff_host + 1;
					}
				}				
			}
		}
		if (count!=0){
			serror_rate=(float)serror/(float)count;
			rerror_rate=(float)rerror/(float)count;
			same_srv_rate=(float)same_srv/(float)count;
			diff_srv_rate=(float)diff_srv/(float)count;
		}
		else{
			serror_rate= (float)0;
			rerror_rate= (float)0;
			same_srv_rate= (float)0;
			diff_srv_rate= (float)0;
		}
		if (srv_count!=0){
			srv_serror_rate=(float)srv_serror/(float)srv_count;
			srv_error_rate=(float)srv_error/(float)srv_count;
			srv_diff_host_rate=(float)srv_diff_host/(float)srv_count;
		}
		else{
			srv_serror_rate= (float)0;
			srv_error_rate= (float)0;
			srv_diff_host_rate= (float)0;
		}
		sprintf(line, "%s %d %d %f %f %f %f %f %f %f", 
							line1, 
							count,srv_count,serror_rate,srv_serror_rate,rerror_rate,srv_error_rate,same_srv_rate,diff_srv_rate,srv_diff_host_rate);
		line[strlen(line)] = '\0';
		strcpy(input[counter],line);

		//last 100 connections
		if(counter<=100){
			counter100=0;
		}
		else{
			counter100=counter-100;
		}
		count=0;
		serror=0;
		rerror=0;
		same_srv=0;
		diff_srv=0;
		srv_count=0;
		srv_serror=0;
		srv_error=0;
		srv_diff_host=0;
		same_src_port=0;
		for(j=counter100; j<counter; j++){
			strcpy(line2, input[j]);
		  sscanf(line2, "%d %s %d %d %s %s %s %s %s %s %s",
		 		&connNum2,&tstamp2s,&orig_p2,&resp_p2,&orig_h2,&resp_h2,
		           	&duration2,&protocol2,&service2,&flag2);
		 	sscanf(tstamp2s, "%d.%d", &tstamp2, &tstamp22);
		  orig_h2[strlen(orig_h2)] = '\0';
		  resp_h2[strlen(resp_h2)] = '\0';
		  service2[strlen(service2)] = '\0';
		  flag2[strlen(flag2)] = '\0';

			if (strcmp(resp_h1,resp_h2)==0){
      	count= count + 1;
        if (strcmp(flag2,"S0")==0 || strcmp(flag2,"S1")==0 || strcmp(flag2,"S2")==0 || strcmp(flag2,"S3")==0){
        	serror= serror + 1;
        }
      	if (strcmp(flag2,"REJ")==0){
      		rerror= rerror + 1;
      	}
        if (strcmp(service2,"other")!=0 && strcmp(service1,service2)==0){
         	same_srv= same_srv + 1;
       	}
        if (strcmp(service1,service2)!=0){
          diff_srv= diff_srv + 1;
        }
   		}
			if (resp_p1==resp_p2){
     		srv_count= srv_count + 1;
        if (strcmp(flag2,"S0")==0 || strcmp(flag2,"S1")==0 || strcmp(flag2,"S2")==0 || strcmp(flag2,"S3")==0){
        	srv_serror= srv_serror + 1;
       	}
        if (strcmp(flag2,"REJ")==0){
        	srv_error= srv_error + 1;
        }
        if (strcmp(resp_h1,resp_h2)!=0){
      		srv_diff_host= srv_diff_host + 1;
       	}
    	}
    	if (orig_p1==orig_p2){
    		same_src_port= same_src_port + 1;
    	}
		}
    if (count!=0){
      serror_rate=(float)serror/(float)count;
      rerror_rate=(float)rerror/(float)count;
      same_srv_rate=(float)same_srv/(float)count;
    	diff_srv_rate=(float)diff_srv/(float)count;
    }
    else{
    	serror_rate= (float)0;
      rerror_rate= (float)0;
      same_srv_rate= (float)0;
     	diff_srv_rate= (float)0;
   	}
		if (srv_count!=0){
			srv_serror_rate=(float)srv_serror/(float)srv_count;
		  srv_rerror_rate=(float)srv_error/(float)srv_count;
		  srv_diff_host_rate=(float)srv_diff_host/(float)srv_count;
		}
		else{
			srv_serror_rate= (float)0;
		  srv_rerror_rate= (float)0;
		  srv_diff_host_rate= (float)0;
		}
		if(counter-counter100!=0)
			same_src_port_rate=(float)same_src_port/(float)(counter-counter100);
		else
			same_src_port_rate=(float)0;

		strcpy(line1, input[counter]);
    sprintf(line, "%s %d %d %f %f %f %f %f %f %f %f",
          		line1, 
    					count,srv_count,same_srv_rate,diff_srv_rate,same_src_port_rate,srv_diff_host_rate,serror_rate,srv_serror_rate,rerror_rate,srv_rerror_rate);
  	line[strlen(line)] = '\0';
   	strcpy(input[counter],line);
	}


	//Write output to file
	sprintf(filename, "trafAld.list");
	ftrafAld = fopen(filename, "w");	
	for(i=0; i<inputCount; i++){
		fprintf(ftrafAld, "%s\n", input[i]);
	}
	fclose(ftrafAld);	
}
