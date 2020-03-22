PROTOCOL FORMAT

String terbagi menjadi 2 bagian dan dipisahkan oleh spasi

```COMMAND [spasi] PARAMETER [spasi] PARAMETER```

#### FITUR
1.  create : Membuat record

    request : create
  
    parameter : nama [spasi] notelpon
  
    response : berhasil -> OK
               gagal -> ERROR

2.  delete : Menghapus record
  
    request: delete
  
    parameter : id
  
    response: berhasil -> OK
             gagal -> ERROR
             
3.  list : untuk melihat daftar record
    
    request: list
    
    parameter: tidak ada
    
    response: daftar record person yang ada
    
4.  get : untuk mencari record berdasar nama
    
    request: get 
  
    parameter: nama yang dicari
  
    response: record yang dicari dalam bentuk json format

```jika command tidak dikenali akan merespon dengan ERRCMD```