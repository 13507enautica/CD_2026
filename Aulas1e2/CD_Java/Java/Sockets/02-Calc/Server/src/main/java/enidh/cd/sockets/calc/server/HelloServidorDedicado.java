package enidh.cd.sockets.calc.server;

/**
 *
 * @author cgonc
 */

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.net.Socket;

/**
 *
 * @author cgonc
 */
public class HelloServidorDedicado extends Thread {

    private final Socket s;

    /**
     * @param s the socket to the client
     */
    public HelloServidorDedicado(Socket s) {
        this.s = s;
        
        System.out.println("Servidor dedicado criado" );
    }

    @Override
    public void run() {
        System.out.printf("Servidor dedicado ativo no endereço %s no porto %d.\n", this.s.getInetAddress().toString(), this.s.getLocalPort() );

        DataInputStream in = null;
        DataOutputStream out = null;
        
        try {
            // ordem inversa do cliente
            in = new DataInputStream( this.s.getInputStream() );
            out = new DataOutputStream( this.s.getOutputStream() );

            for ( ; ;) {
                byte[] responseRAW1 = new byte[ 1024 ];
                byte[] responseRAW2 = new byte[ 1024 ];
                int numBytesRd1 = in.read(responseRAW1 );
                byte oper = in.readByte();
                int numBytesRd2 = in.read(responseRAW2 );
                System.out.printf("\nO OPERADOR LIDO FOI: %s\n",(char)oper);

                if ( numBytesRd1>0 && numBytesRd2>0) {
                    String responseAsString1 = new String(responseRAW1, 0, numBytesRd1);
                    String responseAsString2 = new String(responseRAW2, 0, numBytesRd2);

                    System.out.printf("Responses (RAW format):\n%s\n&\n%s\n", responseAsString1,responseAsString2);

                    ObjectMapper mapper = new ObjectMapper();

                    Complexo response1 = mapper.readValue(responseRAW1, Complexo.class);
                    Complexo response2 = mapper.readValue(responseRAW2, Complexo.class);

                    switch (oper) {
                        case '+':
                            response1 = response1.addTo(response2);
                            break;

                        case '-':
                            response1 = response1.subtractTo(response2);
                            break;

                        case '*':
                            response1 = response1.multiplyBy(response2);
                            break;

                        default:
                            response1 = new Complexo();
                            break;
                    }

                    System.out.printf("Response:\n%s\n", response1);

                    ObjectWriter ow = mapper.writer().withDefaultPrettyPrinter();

                    String dataToSend = ow.writeValueAsString(response1);

                    System.out.printf("Going to send data:\n%s\n", dataToSend);

                    out.write(dataToSend.getBytes());

                }
            }
        }
        catch (java.io.EOFException ioEx) {
            System.out.println( "Ligação fechada." );
        }
        catch (Exception ex) {
            System.err.printf( "Erro no servidor dedicado!\nDetalhes:\n" );
            ex.printStackTrace( System.err );
        }
        finally {
            try {
                if ( in!=null ) {
                    in.close();
                }
                if ( out!=null ) {
                    out.close();
                }
                this.s.close();
            }
            catch (Exception ex) {
                System.err.printf( "Erro ao terminar servidor dedicado!\nDetalhes:\n" );
                ex.printStackTrace( System.err );
            }
        }

        System.out.printf("Servidor dedicado a terminar.\n");
    }
}
