package com.example.a2101179_test;

import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.mlkit.common.model.DownloadConditions;
import com.google.mlkit.nl.translate.TranslateLanguage;
import com.google.mlkit.nl.translate.Translation;
import com.google.mlkit.nl.translate.Translator;
import com.google.mlkit.nl.translate.TranslatorOptions;
import org.jetbrains.annotations.NotNull;

public class t2tFragment extends Fragment {
    // Instantiate our variables
    TextView Source;
    TextView Target;
    Spinner source_spinner;
    Spinner target_spinner;
    Button Translate;
    String sourcetext="";
    Translator generaltranslator;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the t2t fragment onto the screen
        View CurrentFragment = inflater.inflate(R.layout.fragment_t2t, container, false);

        // Select components by finding their ID
        Source = CurrentFragment.findViewById(R.id.Source);
        Target = CurrentFragment.findViewById(R.id.Target);
        Translate = CurrentFragment.findViewById(R.id.button);
        source_spinner = CurrentFragment.findViewById(R.id.spinner);
        target_spinner = CurrentFragment.findViewById(R.id.spinner2);

        // Call function that sets the spinner content full of languages
        SetSpinnerContent(CurrentFragment);

        // Click listener for the Translate button
        Translate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sourcetext=Source.getText().toString();
                // Call function to detect languages and download language model
                language_model_download();
            }
        });
        return CurrentFragment;
    }


    // Set spinner content full of languages
    private void SetSpinnerContent(View view) {
        source_spinner = (Spinner) view.findViewById(R.id.spinner);
        target_spinner = (Spinner) view.findViewById(R.id.spinner2);
        String[] languages = new String[]{
                "English", "Chinese", "French", "German","Italian", "Japanese", "Urdu"
        };
        // Set up an array adapter populate with language array
        // and set them to the spinners
        ArrayAdapter<String> language_adapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_spinner_item, languages);
        source_spinner.setAdapter(language_adapter);
        target_spinner.setAdapter(language_adapter);
    }


    // Function to detect source and target languages and download language model
    // also sets language for text to speech if fragment is s2s or t2s
    private void language_model_download(){
        String sourcelanguage = "";
        String targetlanguage = "";
        // Get spinner language selection
        String firstdropdown = source_spinner.getSelectedItem().toString();
        String seconddropdown = target_spinner.getSelectedItem().toString();
        // Set source language based on spinner entry
        switch (firstdropdown) {
            case "English":
                sourcelanguage = TranslateLanguage.ENGLISH;
                break;
            case "German":
                sourcelanguage = TranslateLanguage.GERMAN;
                break;
            case "French":
                sourcelanguage = TranslateLanguage.FRENCH;
                break;
            case "Urdu":
                sourcelanguage = TranslateLanguage.URDU;
                break;
            case "Chinese":
                sourcelanguage = TranslateLanguage.CHINESE;
                break;
            case "Italian":
                sourcelanguage = TranslateLanguage.ITALIAN;
                break;
            case "Japanese":
                sourcelanguage = TranslateLanguage.JAPANESE;
                break;
        }
        // Set target language and text to speak language based on spinner2 entry
        switch (seconddropdown) {
            case "English":
                targetlanguage = TranslateLanguage.ENGLISH;
                break;
            case "German":
                targetlanguage = TranslateLanguage.GERMAN;
                break;
            case "French":
                targetlanguage = TranslateLanguage.FRENCH;
                break;
            case "Urdu":
                targetlanguage = TranslateLanguage.URDU;
                //No tts for Urdu
                break;
            case "Chinese":
                targetlanguage = TranslateLanguage.CHINESE;
                break;
            case "Italian":
                targetlanguage = TranslateLanguage.ITALIAN;
                break;
            case "Japanese":
                targetlanguage = TranslateLanguage.JAPANESE;
                break;
        }


        // Set source and target languages to translator
        TranslatorOptions language_selection = new TranslatorOptions.Builder().setSourceLanguage(sourcelanguage).setTargetLanguage(targetlanguage).build();
        generaltranslator = Translation.getClient(language_selection);
        // Download required language model if not already downloaded
        DownloadConditions download_criteria = new DownloadConditions.Builder().requireWifi().build();
        generaltranslator.downloadModelIfNeeded(download_criteria).addOnSuccessListener(new OnSuccessListener<Void>() {
            @Override
            public void onSuccess(Void unused) {
                // If model downloaded call translate function
                translateLanguage();
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull @NotNull Exception e) {
                Target.setText("Error");
            }
        });
    }

    // Function for translating source text and putting translated
    // text in the target text view
    private void translateLanguage() {
        // Translate source text
        generaltranslator.translate(sourcetext).addOnSuccessListener(new OnSuccessListener<String>() {
            @Override
            public void onSuccess(String s) {
                // If successful, set target text view to translated text
                Target.setText(s);
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull @NotNull Exception e) {
                Target.setText("Error");
            }
        });
    }
}

