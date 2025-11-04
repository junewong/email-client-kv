# JavaMail
-keep class javax.mail.** { *; }
-keep class javax.activation.** { *; }
-keep class com.sun.mail.** { *; }
-dontwarn javax.mail.**
-dontwarn javax.activation.**

# Room
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-dontwarn androidx.room.paging.**

# Keep data models
-keep class com.example.mailclient.data.model.** { *; }
