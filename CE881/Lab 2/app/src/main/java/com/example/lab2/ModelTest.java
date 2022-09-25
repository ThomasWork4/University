package com.example.lab2;

public class ModelTest {
    public static void main(String[] args) {
        LightsModel model = new LightsModel(5);
        System.out.println(model);
        model.flipLines(2,2);
        System.out.println(model);
        model.flipLines(1,2);
        System.out.println(model);
        model.flipLines(1,1);
        System.out.println(model);
    }
}
