package com.example.a2101179_test;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import androidx.navigation.NavController;
import androidx.navigation.fragment.NavHostFragment;
import androidx.navigation.ui.NavigationUI;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Set our activity_main xml as the screen to load when the app first opens
        setContentView(R.layout.activity_main);


        // Load our bottom navigation bar and attach a navigation host used
        // for navigating each fragment
        BottomNavigationView bottomNavigationView = findViewById(R.id.bottom_navigation_bar);
        NavHostFragment navHostFragment = (NavHostFragment) getSupportFragmentManager().findFragmentById(R.id.fragment_container_view);
        assert navHostFragment != null;
        NavController navController = navHostFragment.getNavController();
        NavigationUI.setupWithNavController(bottomNavigationView, navController);

    }
}