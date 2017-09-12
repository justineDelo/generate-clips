import tensorflow as tf
import numpy as np
import os
classe=[[]]
cls=[525,81,172,339,432,292,75,23,43,331]
for i in range(9):
    classe.append([])


path = "C:\\Users\\Utilisateur\\Documents\\TB1A\\stage\\TensorFlow-Tutorials\\jain-makeba-official-music-videoson"#get_file(dirname, origin=origin, untar=True)
def audioSet(path) :
    """
    labels = sorted([d for d in os.listdir(path)])
    print(labels)
    
    for gh, label in enumerate(labels):
        print(gh, label)
        label_dir = os.path.join(path, label)
        fpaths = np.array([os.path.join(label_dir, img_fname) for img_fname in os.listdir(label_dir)])
        print(fpaths)
        #
        #print(len(transfer_values_imagenet1))
        
        for sa in range(0,len(fpaths)):
            filename = fpaths[sa]
            print(filename[:-4])
            """

    
    #for serialized_example in tf.python_io.tf_record_iterator(filename):
    for serialized_example in tf.python_io.tf_record_iterator(transformVideo(path)):
        
        
        example = tf.train.SequenceExample()
        example.ParseFromString(serialized_example)
        #print(example)
        string=np.zeros([1280],dtype='f')
        intersection=[]
        x=example.context.feature["labels"].int64_list.value
        print('x',x)
        for k in cls:
            for h in x:
                if h==k:
                    intersection.append(cls.index(h))
        print(len(example.feature_lists.feature_list["audio_embedding"].feature))
        if(len(example.feature_lists.feature_list["audio_embedding"].feature)==10 and len(intersection)==1):
            print('if')
            for i in range(10):
     
                a=example.feature_lists.feature_list["audio_embedding"].feature[i].bytes_list.value[0]
                for j in range(len(a)):
                    string[j+i*128]=float(a[j])    
               
            classe[intersection[0]].append(string)
                
    for k in range(10):
        fil=np.asarray(classe[k])
        print(fil)
                #print(fil.shape)
        fil.tofile("feat"+str(k)+"sound.bit")
    print(classe)
    return fil 

def transformVideo(path = "song.wav") :
    from scipy.io.wavfile import read
    import numpy 
    import tensorflow as tf
    
    
    def _bytes_feature(value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))
    
    def _int64_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
    
    tfrecords_filename = 'tfrec.tfrecords'
    writer = tf.python_io.TFRecordWriter(tfrecords_filename)
    for element in os.listdir(path):
        if( not os.path.isdir(element)):
            a = read(path+'\\'+element)
            
            matrix =np.array(a[1])
            
            height = matrix.shape[0]
            width = matrix.shape[1]
            
            
            
            img_raw = matrix.tostring()
            
            
            
            example = tf.train.Example(features=tf.train.Features(feature={
                'height': _int64_feature(height),
                'width': _int64_feature(width),
                'image_raw': _bytes_feature(img_raw)}))
            
            writer.write(example.SerializeToString())
            
    writer.close()
    print(tfrecords_filename)
    return tfrecords_filename

            
            
#    tensor = tf.stack(matrix)
#    tf.InteractiveSession()
#    evaluated_tensor = tensor.eval()

#    import wave
#    
#    w = wave.open(path, "rb")
#    binary_data = w.readframes(w.getnframes())
#    w.close()


   
    
    
    


    


    
