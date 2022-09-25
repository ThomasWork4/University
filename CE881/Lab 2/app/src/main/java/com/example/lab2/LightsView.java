package com.example.lab2;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;

public class LightsView extends View implements View.OnClickListener, View.OnTouchListener {

    static int bg = Color.BLACK;
    static int bgGrid = Color.BLUE;
    static int fgOff = Color.DKGRAY;
    static int fgOn = Color.YELLOW;
    static int[] cols = {fgOff, fgOn};
    static String tag = "LightsView: ";
    LightsModel model;
    int size;
    int n;
    int xOff, yOff, minLen, gridSquareLen;

    public LightsView(Context context) {
        super(context);
        setup(context, "Constructor 1");
    }

    public LightsView(Context context, LightsModel model) {
        super(context);
        this.model = model;
        setup(context, "Constructor 1a");
    }

    public LightsView(Context context, AttributeSet attrs) {
        super(context, attrs);
        setup(context, "Constructor 2");
    }

    public LightsView(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        setup(context, "Constructor 3");
    }

    private void setup(Context context, String cons) {
        System.out.println(tag + cons);
        checkModel();
        setOnTouchListener(this);
        setOnClickListener(this);
    }

    private void checkModel() {
        if (model != null) {
            n = model.n;
        } else {
            System.out.println(tag + "Oops: Null model");
            n = 5;
            model = new LightsModel(n);
        }
    }

    private void SetGeometry() {
        int midX = getWidth() / 2;
        int midY = getHeight() / 2;
        minLen = Math.min(getWidth(), getHeight());

        gridSquareLen = (minLen / n) * n;

        size = gridSquareLen / n;
        xOff = midX - gridSquareLen / 2;
        yOff = midY - gridSquareLen / 2;
    }

    public void draw(Canvas g) {
        super.draw(g);
        Paint p = new Paint();
        p.setAntiAlias(true);
        p.setStyle(Paint.Style.FILL);
        p.setColor(bg);
        SetGeometry();

        g.drawRect(0, 0, getWidth(), getHeight(), p);
        p.setColor(bgGrid);
        g.drawRoundRect(new RectF(xOff, yOff, xOff + gridSquareLen, yOff + gridSquareLen), 5, 5, p);

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                int cx = xOff + size * i + size / 2;
                int cy = yOff + size * j + size / 2;
                p.setColor(cols[model.grid[i][j]]);
                drawTile(g, cx, cy, p);
            }
        }
    }

    private void drawTile(Canvas g, int cx, int cy, Paint p ) {
        int length = (size * 7) / 8;
        int rad = size / 6;
        int x = cx - length / 2;
        int y = cy - length / 2;

        RectF rect = new RectF(x,y,x+length,y+length);
        g.drawRoundRect(rect,rad,rad,p);
    }

    @Override
    public void onClick(View view) {
        int i = (int) ((curX - xOff) / size);
        int j = (int) ((curY - yOff) / size);
        model.getScore();
        model.tryFlip(i,j);
        postInvalidate();
    }

    float curX, curY;

    @Override
    public boolean onTouch(View view, MotionEvent motionEvent) {
        curX = motionEvent.getX();
        curY = motionEvent.getY();
        return false;
    }
}
