package enidh.cd.sockets.calc.server;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

public class Complexo {

    private final int real;
    private final int imaginary;

    public Complexo() {this(0,0);}

    @JsonCreator
    public Complexo(@JsonProperty("real") int real, @JsonProperty("imaginary") int imaginary){
        this.real = real;
        this.imaginary = imaginary;
    }

    public String toString(){
        return "" + this.real + " + " + this.imaginary + "i";
    }

    public int getReal(){
        return this.real;
    }

    public int getImaginary(){
        return this.imaginary;
    }

    public Complexo addTo(Complexo number){
        return new Complexo(this.real + number.getReal(), this.imaginary + number.getImaginary());
    }

    public Complexo subtractTo(Complexo number){
        return new Complexo(this.real - number.getReal(), this.imaginary - number.getImaginary());
    }

    public Complexo multiplyBy(Complexo number){
        /*System.out.printf("Número real: %d\n",(this.real*number.getReal() - this.imaginary* number.getImaginary()));
        System.out.printf("Número imaginário: (%d * %d) + (%d * %d) = %d\n",
                this.real, number.getImaginary(), this.imaginary, number.getReal(),
                (this.real*number.getImaginary() + this.imaginary* number.getReal()));*/
        return new Complexo((this.real*number.getReal() - this.imaginary* number.getImaginary()), (this.real*number.getImaginary() + this.imaginary* number.getReal()));
    }
}
