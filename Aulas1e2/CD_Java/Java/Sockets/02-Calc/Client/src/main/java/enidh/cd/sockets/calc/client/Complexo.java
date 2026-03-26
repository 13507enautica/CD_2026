package enidh.cd.sockets.calc.client;

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
        return new Complexo((this.real*number.getReal() - this.imaginary* number.getImaginary()), (this.real*number.getImaginary() + this.imaginary* number.getReal()));
    }
}
