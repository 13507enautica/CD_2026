package enidh.cd.sockets.calc.client;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

/**
 *
 * @author cgonc
 */
public class App extends Thread {
    
    private static final String DefaultHostName = "localhost";
    
    private static final int DefaultPort = 12345;
    
    private Socket s;
    
    public App(String host, int port) {
        try {
            this.s = new Socket(host, port);
 
            System.out.printf("Ligação estabelecida (%s).\n", this.s.toString());
        } catch (Exception e) {
            this.s = null;

            System.out.printf("Não foi possível estabelecer ligação com o servidor (%s) no porto pretendio (%d)\nDetalhes:\n", host, port);
            e.printStackTrace(System.err);
        }
    }
    
    private void sendArgs(DataOutputStream out, int op1, int op2, int op3, int op4, byte oper) throws IOException {

        Complexo num_complexo1 = new Complexo(op1,op2);
        Complexo num_complexo2 = new Complexo(op3,op4);

        ObjectMapper mapper = new ObjectMapper();

        ObjectWriter ow = mapper.writer().withDefaultPrettyPrinter();

        String dataToSend1 = ow.writeValueAsString(num_complexo1);
        String dataToSend2 = ow.writeValueAsString(num_complexo2);

        System.out.printf( "Going to send data:\n%s\n & \n%s\n", dataToSend1, dataToSend2);

        out.write( dataToSend1.getBytes() );
        out.writeByte( oper );
        out.write( dataToSend2.getBytes() );

        /*out.writeInt( op1 );
        out.writeInt( op2 );
        out.writeByte( oper );*/
        
        out.flush();
    }
    
    private void showResponse(DataInputStream in, int op1, int op2, char oper, int op3, int op4) throws IOException {

        byte[] responseRAW = new byte[1024];
        int numBytesRd = in.read(responseRAW);

        if (numBytesRd > 0) {
            String responseAsString = new String(responseRAW, 0, numBytesRd);

            System.out.printf("Response (RAW format):\n%s\n", responseAsString);

            ObjectMapper mapper = new ObjectMapper();

            Complexo response = mapper.readValue(responseRAW, Complexo.class);

            System.out.printf("Response:\n%d + %di %c %d + %di = %s\n",op1, op2, oper, op3, op4, response);
        }
    }
    
    @Override
    public void run() {
        if (this.s != null) {
            try {
                DataOutputStream out = new DataOutputStream(this.s.getOutputStream());

                int op1=2, op2=1, op3=3, op4=2;
                char oper1, oper2, oper3;

                sendArgs(out, op1, op2, op3, op4, (byte) (oper1 = '+'));
                sendArgs(out, op1, op2, op3, op4, (byte) (oper2 = '-'));
                sendArgs(out, op1, op2, op3, op4, (byte) (oper3 = '*'));

                DataInputStream in = new DataInputStream(this.s.getInputStream());

                showResponse(in, op1, op2, oper1, op3, op4);
                showResponse(in, op1, op2, oper2, op3, op4);
                showResponse(in, op1, op2, oper3, op3, op4);

                out.close();
                in.close();
                s.close();

            } catch (Exception e) {
                System.out.printf("Erro ao processar mensagens.\nDetalhes:\n");
                e.printStackTrace(System.err);
            }

            System.out.printf("Cliente a terminar.\n");
        }
    }

    /**
     * @param args the command line arguments
     *
     * args[0] is the host name (string) 
     * args[1] is the port number (integer)
     */
    public static void main(String[] args) {
        String host = (args.length>=1) ? args[0] : DefaultHostName; 
        int port = (args.length>=2) ? Integer.parseInt( args[1] ) : DefaultPort;

        App cli = new App(host, port );
        cli.start();

        System.out.println("Função main do cliente a terminar...");
    }
    
}
