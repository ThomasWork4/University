package com.example.lab2;

import android.view.View;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {

    static int n = 7;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //setContentView(new LightsView(this, new LightsModel(n)));
        setContentView(R.layout.sample_lights_view);

        Thread thread = new Thread() {

            @Override
            public void run() {
                try {
                    while (!isInterrupted()) {
                        Thread.sleep(1000);
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                LightsView lightsView = (LightsView) findViewById(R.id.lightsView);
                                TextView score = (TextView) findViewById(R.id.textView);
                                int newScore = lightsView.model.getScore();
                                System.out.println(newScore);
                                score.setText("Your Current Score is " + Integer.toString(newScore));
                                if (lightsView.model.isSolved()) {
                                    score.setText("Well done you've Won!!");
                                }
                            }
                        });
                    }
                } catch (InterruptedException e) {
                }
            }
        };

        thread.start();
    }

    public void resetModel (View view) {
        LightsView lightsView = (LightsView) findViewById(R.id.lightsView);
        lightsView.model.reset();
        lightsView.postInvalidate();
    }


}