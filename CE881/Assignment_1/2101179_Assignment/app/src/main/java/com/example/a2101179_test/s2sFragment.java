package com.example.a2101179_test;

import android.app.Activity;
import android.content.Intent;
import android.speech.tts.TextToSpeech;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.widget.*;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.mlkit.common.model.DownloadConditions;
import com.google.mlkit.nl.translate.*;
import org.jetbrains.annotations.NotNull;
import java.util.ArrayList;
import java.util.Locale;
import java.util.Objects;

public class s2sFragment extends Fragment {
    // Instantiate our variables
    TextView Source;
    TextView Target;
    ImageButton Mic_Button;
    TextToSpeech text2speech;
    // Request code for voice recognition
    private static final int REQUEST_CODE_SPEECH_INPUT = 1;
    Spinner source_spinner;
    Spinner target_spinner;
    Button Translate;
    String sourcetext="";
    Translator generaltranslator;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        // Inflate the s2s fragment onto the screen
        View CurrentFragment = inflater.inflate(R.layout.fragment_s2s, container, false);

        // Select components by finding their ID
        Source = CurrentFragment.findViewById(R.id.Source);
        Target = CurrentFragment.findViewById(R.id.Target);
        Translate = CurrentFragment.findViewById(R.id.button);
        Mic_Button = CurrentFragment.findViewById(R.id.imageButton2);
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


        // On click listener used for our microphone button
        Mic_Button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Instantiate speech recognition intent
                Intent speech_recognition = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                speech_recognition.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                speech_recognition.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
                speech_recognition.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to Speech");
                try {
                    // Request permission code
                    startActivityForResult(speech_recognition, REQUEST_CODE_SPEECH_INPUT);
                }
                catch (Exception e) {
                    // Pop up for clarity purposes
                    Toast.makeText(s2sFragment.this.getActivity(), " " + e.getMessage(),Toast.LENGTH_SHORT).show();}}
        });
        return CurrentFragment;
    }


    @Override
    // Called when audio has finished being detected
    public void onActivityResult(int requestCode, int resultCode, @Nullable Intent data)
    {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CODE_SPEECH_INPUT) {
            if (resultCode == Activity.RESULT_OK && data != null) {
                // If there was an input, store all possible language results in array
                ArrayList<String> possible_results = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                // Choose the most likely option and set source text accordingly
                Source.setText(Objects.requireNonNull(possible_results).get(0));
            }
        }}


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
    public void language_model_download(){
        String sourcelanguage = "";
        String targetlanguage = "";
        Locale outputlanguage = Locale.ENGLISH;
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
                outputlanguage = Locale.ENGLISH;
                break;
            case "German":
                targetlanguage = TranslateLanguage.GERMAN;
                outputlanguage = Locale.GERMAN;
                break;
            case "French":
                targetlanguage = TranslateLanguage.FRENCH;
                outputlanguage = Locale.FRENCH;
                break;
            case "Urdu":
                targetlanguage = TranslateLanguage.URDU;
                //No tts for Urdu
                break;
            case "Chinese":
                targetlanguage = TranslateLanguage.CHINESE;
                outputlanguage = Locale.CHINESE;
                break;
            case "Italian":
                targetlanguage = TranslateLanguage.ITALIAN;
                outputlanguage = Locale.ITALIAN;
                break;
            case "Japanese":
                targetlanguage = TranslateLanguage.JAPANESE;
                outputlanguage = Locale.JAPANESE;
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

            // Instantiate our text to speech object and set the language
            Locale finalOutputlanguage = outputlanguage;
            text2speech = new TextToSpeech(getActivity(), new TextToSpeech.OnInitListener() {
                        @Override
                        public void onInit(int i) {
                            if (i != TextToSpeech.ERROR)
                            {
                                text2speech.setLanguage(finalOutputlanguage);
                            }
                        }
                    });
    }

    // Function for translating source text and putting translated
    // text in the target text view
    public void translateLanguage() {
        // Translate source text
        generaltranslator.translate(sourcetext).addOnSuccessListener(new OnSuccessListener<String>() {
            @Override
            public void onSuccess(String s) {
                // If successful, set target text view to translated text
                Target.setText(s);
                String target_text = Target.getText().toString();
                // Output the result using text to speech
                text2speech.speak(target_text,TextToSpeech.QUEUE_FLUSH,null,null);
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull @NotNull Exception e) {
                Target.setText("Error");
            }
        });
    }

}

